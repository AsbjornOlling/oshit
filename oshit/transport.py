# python imports
import socket
import threading

# application imports
import packet


class Transport:
    """ Implementation of the oSHIT transport protocol
    for tcp-like flow control and error control
    over udp.
    """
    WSIZE = 128  # MAX windowsize

    def __init__(self, CONNECT_ADDR=None, LOCAL_ADDR=None, logic=None):
        # general utility imports
        self.logic = logic
        self.oSHIT = logic.oSHIT
        self.config = logic.config
        self.logger = logic.logger

        # address to open socket on
        self.LOCAL_ADDR = LOCAL_ADDR
        self.LOCAL_IP, self.LOCAL_PORT = LOCAL_ADDR
        # address to connect to
        self.CONNECT_ADDR = CONNECT_ADDR
        self.CONNECT_IP, self.CONNECT_PORT = CONNECT_ADDR

        # init lists and counters
        # Rx
        self.rxbuffer = []      # for packets out of order
        self.rxmin = 0
        self.rxmax = self.rxmin + self.WSIZE
        # Tx
        self.txwindow = []      # packets to transmit
        self.txbuffer = []      # for all transmitted packets (keep until ACK)
        self.lastreceived = -1  # counter for SEQ of last received payload
        self.txmin = 0          # transmission window bounds
        self.txmax = self.txmin + self.WSIZE  # default bounds = [0, 128[

        # start socket
        self.sock = self.create_socket()

        # i/o objs (they manage the socket)
        self.rx = Incoming(transport=self)
        self.tx = Outgoing(transport=self)

        # START SHIT
        # TODO handle closing socket
        # Start InPacket processor thread
        self.proc = self.start_processorthread()

        # connect to something
        self.connect(self.CONNECT_ADDR)

    def create_socket(self):
        """ Create a UDP socket """
        self.logger.log(2, "Starting socket")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind(self.LOCAL_ADDR)
        return sock

    def connect(self, addr):
        """ Just connect the socket to an (address, port) tuple """
        self.logger.log(2, "Connecting to "
                        + str(addr[0]) + ":" + str(addr[1]))
        self.sock.connect(addr)

    def start_processorthread(self):
        """ Starts thread on self.process_incoming()
        The thread reads InPackets from rxqueue,
        and is woken by Incoming when new packets arrive.
        """
        self.logger.log(3, "Starting transport in-processor.")
        proc = threading.Thread(target=self.process_incoming,
                                args=(self.rx.rxqueue, self.rx.rxlock),
                                name="Transport processor thread")
        proc.start()
        return proc

    def process_incoming(self, rxqueue, rxlock):
        """ Processes incoming packet object (InPacket).
        Call Selective-Reject logic if ACK or NACK,
        otherwise pass it on to application logic.
        This method runs in a thread, which sleeps
        until the Incoming object updates its rxqueue.
        """
        # TODO: close when socket closes
        while True:
            # take first packet from list
            if rxqueue:
                pck = rxqueue.pop(0)  # threadsafe
                if pck.ACK:
                    self.in_ack(pck)
                elif pck.NACK:
                    self.in_nack(pck)
                else:
                    self.in_payload(pck)
            else:
                rxlock.acquire()
                rxlock.wait()  # wait for new item to arrive

    def in_ack(self, ackpck):
        """ Handle incoming ACK packets.
        Remove all packets with SEQ less than the ACK's SEQ.
        (As we know that they're properly received.)
        """
        ackseq = ackpck.SEQ
        for bufpck in self.txbuffer[:]:  # copy of list to avoid mutation
            if bufpck.SEQ < ackseq:
                # remove accepted packets from buffer
                self.txbuffer.remove(bufpck)
                self.txmax = (self.txmax + 1) % 256
                # TODO: notify Logic._outloop of packetspace

    def in_nack(self, nackpck):
        """ Handle incoming NACK packets.
        Find packet with the NACK's SEQ, and retransmit it.
        """
        nackseq = nackpck.SEQ
        self.logger.log(2, "Received NACK: " + str(nackseq)
                        + ". Re-transmitting.")
        for bufpck in self.txbuffer:
            if bufpck.SEQ == nackseq:
                # re-transmit (cut the queue)
                self.tx.txlock.acquire()
                self.tx.txqueue.insert(0, bufpck)
                self.tx.txlock.notify()
                self.tx.txlock.release()

    def in_payload(self, paypck):
        """ Handle incoming packet with payload.
        This is all packets that aren't ACK or NACK.
        Check if the SEQ is in order, before passing
        on to application layer logic.
        """
        err = False
        # test window bounds
        if not self.check_rxbounds(paypck):
            # error logging for this in self.check_rxbounds
            err = True

        # (if the packet is out of order
        # or if there are out of order packets in buffer)
        # and packet is within window
        if ((paypck.SEQ != (self.lastreceived + 1) % 256
           or self.rxbuffer) and not err):
            err = True
            self.logger.log(2, "Packet arrived out of order.")
            # redirect packet to rxbuffer
            self.in_unordered(paypck)
            # TODO
            # have logic to empty rxbuffer

        # if packet passed checks
        if not err:
            self.in_validpack(paypck, sendack=True)

    def check_rxbounds(self, pck):
        """ Check if InPacket is within rx window bounds.
        Also handles cases where rxmax has "rolled over" to be less than rxmin.
        """
        seq = pck.SEQ
        withinbounds = False  # assume false until determined
        if self.rxmin < self.rxmax:
            if self.rxmin <= seq and seq < self.rxmax:
                withinbounds = True
        elif self.rxmax < self.rxmin:  # weird roll-over edgecase
            if seq < self.rxmax or seq >= self.rxmin:
                withinbounds = True

        # if packet outside bounds
        if not withinbounds:
            self.logger.log(0, "Packet with SEQ " + str(seq)
                            + " is outside window bounds: "
                            + "[" + str(self.rxmin)
                            + ":" + str(self.rxmax) + "[")
        # return bounds state
        return withinbounds

    def in_validpack(self, pck, sendack=False):
        """ Pass packet on to logic module.
        Is called if incoming packet is the next expected packet
        and incoming packet is within rx window bounds.
        """
        # update rxbounds
        self.rxmin = (self.rxmin + 1) % 256
        self.rxmax = (self.rxmax + 1) % 256  # TODO Laarss... why after ack

        # update SEQ count (will always be in 0-255)
        self.lastreceived = pck.SEQ

        # hand over to Logic
        self.logic.tr_new_incoming(pck)

        # send the ACK
        if sendack:
            self.send_ack((pck.SEQ + 1) % 256)

    def in_unordered(self, pck):
        """Handle packet arriving out of order.
        Add the packet in the correct position of self.rxbuffer,
        and check if the next expected packet has come to self.rxbuffer yet.
        This is the only method that interacts with self.rxbuffer.
        """
        self.logger.log(3, "Bufferring packet with SEQ: " + str(pck.SEQ))

        if not self.rxbuffer:
            self.logger.log(3, "rxbuffer was empty. Adding first packet.")
            self.send_ack(nack=True, seq=self.lastreceived + 1)

        # add to (unsorted) buffer
        self.rxbuffer.append(pck)

        # check for the expected packet
        # start emptying buffer if the missing packet is in the buffer
        self.unbuffer_expected()

    def unbuffer_expected(self, level=0):
        """ Removes all packets with ordered SEQs from the buffer.
        It searches for a valid SEQ, then recursively searches for
        another valid packet when another valid is found.
        """
        self.logger.log(3, "Unbuffering: Searching for packet with SEQ: "
                        + str((self.lastreceived + 1) % 256) + " in buffer.")

        # search for packet with appropriate seq
        found = False
        for bufpck in self.rxbuffer[:]:
            if bufpck.SEQ == (self.lastreceived + 1) % 256:
                found = True
                validpck = bufpck
                break
            else:
                self.logger.log(3, "Unbuffering: "
                                + "packet with SEQ " + str(bufpck.SEQ)
                                + " not a match")

        # accept found packet
        if found:
            self.logger.log(3, "Unbuffering: Accepting packet with SEQ: "
                            + str(validpck.SEQ))
            self.in_validpack(validpck, sendack=False)
            self.rxbuffer.remove(validpck)
            # recurse to look for next packet
            self.unbuffer_expected(level=level + 1)

        if level == 0 and found:
            self.logger.log(3, "Unbuffering: Ended. Sending ACK.")
            self.send_ack((self.lastreceived + 1) % 256)

    def send_ack(self, seq, nack=False):
        """ Queues ACK packet with the argument as SEQ for sending.
        Sends nack instead, if nack=True option is set.
        """
        # don't ACK if NACK is set
        ack = False if nack else True

        if ack:
            self.logger.log(3, "Sending ACK: " + str(seq))
        elif nack:
            self.logger.log(3, "Sending NACK: " + str(seq))

        # create ACK packet with empty payload
        ackpck = packet.OutPacket(seq=seq, ack=ack, nack=nack,
                                  oSHIT=self.oSHIT)

        # notify Outgoing thread, and queue the ACK packet
        self.tx.txlock.acquire()
        self.tx.txqueue.append(ackpck)
        self.tx.txlock.notify()
        self.tx.txlock.release()

    def send_payload(self, pck):
        """ Called by Logic, adds a new packet to for transmission. """
        # calculate and set SEQ
        seq = self.txmin + len(self.txwindow)
        pck.set_seq(seq)

        # add to window
        self.txwindow.append(pck)

        # add to txqueue and notify Outgoing
        self.tx.txlock.acquire()
        self.tx.txqueue.append(pck)
        self.tx.txlock.notify()
        self.tx.txlock.release()


class Incoming(threading.Thread):
    """ Class to receive and process incoming packets """
    BSIZE = packet.Packet.HSIZE + packet.Packet.PSIZE  # recv buffersize

    def __init__(self, transport=None):
        # run thread constructor
        threading.Thread.__init__(self)

        # inherit objects
        self.parent = transport
        self.oSHIT = transport.oSHIT
        self.logger = self.oSHIT.logger
        self.sock = transport.sock

        # list of packets that transport reads from
        self.rxqueue = []
        # condition to notify Transport of new Packets in rxqueue
        self.rxlock = threading.Condition()

        # list of current parser threads
        # useful to ensure sequential appending to rxqueue
        self.pthreads = []

        # start threadloop
        # TODO place this elsewhere
        # TODO handle closing sockets
        self.reading = True
        self.start()

    def run(self):
        """ Thread loop """
        self.logger.log(2, "Starting socket read loop.")
        while self.reading:
            # get data from socket (blocking)
            data, addr = self.read()

            # make packet obj concurrently
            parserthread = threading.Thread(name="Packet parser thread",
                                            target=self.parse,
                                            args=([data], self.pthreads))
            parserthread.start()
            self.pthreads.append(parserthread)

    def read(self):
        """ Reads one incoming packet from UDP socket.
        Buffersize set to the maximum packet size.
        """
        data, ancdata, msg_flags, address = self.sock.recvmsg(self.BSIZE)
        self.logger.log(3, "Read data on socket: " + str(type(data)))
        return data, address

    def parse(self, data, threads):
        """ Generate packet objects from raw data.
        Is thread safe, and should cause no concurrency issues.
        """
        # get list of other active threads
        otherthreads = threads[:]
        self.logger.log(3, "Other active parserthreads: "
                        + str(len(otherthreads)))

        # parse the data
        pck = packet.InPacket(data, oSHIT=self.oSHIT)

        self.logger.log(3, "Packet object created.")

        # wait for all previously started threads to complete
        for thread in otherthreads:
            thread.join()

        # guaranteed sequential append
        self.logger.log(3, "Data parser thread adding Packet to rxqueue")
        self.rxlock.acquire()
        self.rxqueue.append(pck)
        self.rxlock.notify()  # notify transport
        self.rxlock.release()
        self.logger.log(3, "Terminating data parser thread")


class Outgoing(threading.Thread):
    """ Class to process and transmit outgoing packets """
    def __init__(self, transport=None):
        # inherited constructor
        threading.Thread.__init__(self, name="Sender thread")

        # inherited objects
        self.parent = transport
        self.oSHIT = transport.oSHIT
        self.logger = transport.logger
        self.sock = transport.sock

        # list of packets that Transport adds to
        self.txqueue = []
        # condition for Transport to notify Outgoing of new packets
        self.txlock = threading.Condition()

        # START SHIT
        self.start()

    def run(self):
        """ Thread method """
        self.write(self.txqueue, self.txlock)  # start sending loop

    def write(self, txqueue, txlock):
        """ Write packets in a loop.
        Gets notified by Transport when a new packet is added.
        Also sets transmission time for packets, useful for detecting timeout.
        """
        # TODO: handle closing socket
        while True:
            if txqueue:  # if list has element
                # get first packet from queue
                pck = txqueue.pop(0)

                # set transmission time and transmit
                pck.set_txtime()  # TODO: implement
                self.sock.sendall(pck.get_bytes())

                # remove from window and update bounds
                # only for payload packets with tracked SEQ
                if pck in self.parent.txwindow:
                    self.parent.txwindow.remove(pck)
                    self.parent.txbuffer.append(pck)
                    self.parent.txmin = (self.parent.txmin + 1) % 256
            else:  # if empty, wait for element to be added
                txlock.acquire()
                txlock.wait()
                txlock.release()  # ?


if __name__ == '__main__':
    pass
