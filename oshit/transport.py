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
    WSIZE = 128  # windowsize

    def __init__(self, CONNECT_ADDR=None, LOCAL_ADDR=None, logic=None):
        # general utility imports
        self.logic = logic
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
        # self.rxwindow = []      # packets to receive TODO remove?
        self.rxbuffer = []      # for packets out of order
        self.rxmin = 0
        self.rxmax = 0
        # Tx
        self.txwindow = []      # packets to transmit (keep until ACK'ed)
        self.lastreceived = -1  # counter for SEQ of last received payload
        self.txmin = 0          # transmit window bounds
        self.txmax = self.txmin + self.WSIZE  # TODO: remove these?

        # start socket
        self.sock = self.create_socket()

        # i/o objs (they manage the socket)
        self.rx = Incoming(transport=self)
        self.tx = Outgoing(transport=self)

        # START SHIT
        # TODO handle closing socket
        threading.Thread(target=self.process_incoming,
                         args=(self.rx.rxqueue, self.rx.rxlock))
        self.connect(self.CONNECT_ADDR)

    def create_socket(self):
        """ Create a UDP socket """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind(self.LOCAL_ADDR)
        return sock

    def connect(self, addr):
        """ Just connect the socket to an (address, port) tuple """
        self.sock.connect(addr)

    def send(self, pck):
        """ Send a packet object.
        To be called by the business logic.
        """
        # TODO
        # add to window
        pass

    def process_incoming(self, rxqueue, rxlock):
        """ Processes incoming packet object.
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
        for winpck in self.txwindow[:]:  # copy of list to avoid mutation
            if winpck.SEQ < ackseq:
                # remove accepted packets from window
                self.txwindow.remove(winpck)
                self.txmax = self.txmax + 1
                # TODO: get new OutPacket from logic

    def in_nack(self, nackpck):
        """ Handle incoming NACK packets.
        Find packet with the NACK's SEQ, and retransmit it.
        """
        nackseq = nackpck.SEQ
        self.logger.log(2, "Received NACK: " + str(nackseq)
                        + ". Re-transmitting.")
        for winpck in self.txwindow:
            if winpck.SEQ == nackseq:
                # re-transmit (cut the queue)
                self.tx.txqueue.insert(0, winpck)

    def in_payload(self, paypck):
        """ Handle incoming packet with payload.
        This is all packets that aren't ACK or NACK.
        Check if the SEQ is in order, before passing
        on to application layer logic.
        """
        # TODO:
        # - is it within window bounds?
        #   - LAAAAAaarrss...

        # if the packet is out of order
        if paypck.SEQ != self.lastreceived + 1:
            # TODO start the rxbuffer SH!T
            pass

        # send ACK
        # self.send_ack(paypck.SEQ + 1)

        # update SEQ count
        self.lastreceived = paypck.SEQ

        # call self.logic.recv_packet()

    def test_write(self):
        # TEST WRITE
        self.logger.log(2, "Starting test datawrite")
        self.sock.connect((self.TEST_IP, self.TEST_PORT))
        self.sock.sendall(bytes("wow", "utf-8"))


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
        while self.reading:
            # get incoming data (blocking)
            data, addr = self.read()

            # make packet obj concurrently
            threading.Thread(target=self.parse,
                             args=(data,
                                   self.rxqueue,
                                   self.rxlock,
                                   self.pthreads)
                             ).start()

    def read(self):
        """ Reads one incoming packet from UDP socket. """
        data, ancdata, msg_flags, address = self.sock.recvmsg(self.BSIZE)
        return data, address

    def parse(self, data, rxqueue, rxlock, pthreads):
        """ Generate packet objects from raw data.
        Is thread safe, and should cause no concurrency issues.
        """
        # copy pthreads, to have alist of only other threads
        otherthreads = pthreads[:]
        pthreads.append(self)  # add this thread to pthreads

        # parse the data
        pck = packet.InPacket(data)

        # wait for all previously started threads to complete
        for thread in otherthreads:
            thread.join()
        # guaranteed sequential append
        rxlock.acquire()
        rxqueue.append(pck)
        rxlock.notify()  # notify transport
        rxlock.release()


class Outgoing(threading.Thread):
    """ Class to process and transmit outgoing packets """
    def __init__(self, transport=None):
        # inherited constructor
        threading.Thread.__init__(self)

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
                pck = txqueue.pop(0)
                pck.set_txtime()                    # TODO: implement
                self.sock.sendall(pck.get_bytes())  # TODO: implement
                self.parent.txmin = self.parent.txmin + 1
            else:  # if empty, wait for element to be added
                txlock.acquire()
                txlock.wait()


if __name__ == '__main__':
    # JUST DEBUGGAN
    import oshit
    t = Transport(oshit.oSHIT())
