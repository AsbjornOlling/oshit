# python imports
import socket
import threading

# application imports
import packet


class Transport():
    """ Implementation of the oSHIT transport protocol
    for tcp-like flow control and error control
    over udp.
    """
    WSIZE = 128  # windowsize

    # TODO replace with config values
    LOCAL_IP = "127.0.0.1"
    LOCAL_PORT = 9999

    def __init__(self, oSHIT):
        # general utility imports
        self.oSHIT = oSHIT
        self.config = oSHIT.config
        self.logger = oSHIT.logger

        # init lists
        self.window = []
        self.rxbuffer = []

        # init socket
        self.sock = self.create_socket()

        # i/o objs
        self.rx = Incoming(transport=self)
        self.tx = Outgoing(transport=self)

    def create_socket(self):
        """ Create a UDP socket """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind((self.LOCAL_IP, self.LOCAL_PORT))
        return sock

    def get_timeout(self):
        # TODO
        """ Calculates the optimal timeout in milis,
        based on a moving average of the round trip time so far.
        Temporarily, it just outputs a constant.
        """
        return 100

    def test_write(self):
        # TEST WRITE
        self.logger.log(2, "Starting test datawrite")
        self.sock.connect((self.TEST_IP, self.TEST_PORT))
        self.sock.sendall(bytes("wow", "utf-8"))


class Incoming(threading.Thread):
    """ Class to receive and process incoming packets """
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
                             args=(data, self.rxqueue, self.pthreads)
                             ).start()

    def read(self):
        """ Reads incoming data from UDP socket.
        Runs in a threaded loop.
        """
        return self.sock.recvfrom(1024)  # TODO evaluate this buffersize

    def parse(self, data, rxqueue, pthreads):
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
        rxqueue.append(pck)


class Outgoing(threading.Thread):
    """ Class to process and transmit outgoing packets """
    def __init__(self, transport=None):
        # inherited constructor
        threading.Thread.__init__(self)

        # other app ojbects
        self.parent = transport
        self.oSHIT = transport.oSHIT
        self.logger = self.oSHIT.logger

        # inherited socket
        self.sock = socket


if __name__ == '__main__':
    # JUST DEBUGGAN
    import oshit
    t = Transport(oshit.oSHIT())
