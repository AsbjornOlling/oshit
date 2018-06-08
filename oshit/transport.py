# python imports
import socket
import threading

# application imports
from packet import Packet


class Transport():
    """ Implementation of the oSHIT transport protocol
    for tcp-like flow control and error control
    over udp.
    """
    WSIZE = 128  # windowsize

    # TODO replace with config
    LOCAL_IP = "127.0.0.1"
    LOCAL_PORT = 9999

    def __init__(self, oSHIT):
        # general utility imports
        self.oSHIT = oSHIT
        self.config = oSHIT.config
        self.logger = oSHIT.logger

        # init lists
        self.window = []
        self.txqueue = []
        self.rxbuffer = []

        # create socket
        self.sock = self.create_socket()

        # start threading

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

    def start_threads(self):
        """ Creates and starts rxthread and txthread. """
        self.logger.log(2, "Starting read and write threads")
        # create threads on methods
        self.rxthread = threading.Thread(target=self.sock_read)
        self.txthread = threading.Thread(target=self.sock_write)
        # start threads
        self.rxthread.start()
        self.txthread.start()

    def sock_read(self):
        """ Reads incoming data from UDP socket.
        Runs in a threaded loop.
        """
        while True:
            print("WOW")
            # data = self.sock.recvfrom(1024)  # TODO evaluate this buffersize
            # self.handle_incoming(data)

    def sock_write(self):
        """ Sends any queued packets over UDP.
        Runs in a threaded loop.
        """
        pass

    def handle_incoming(self, data):
        """ Determines type and appropriate action for incoming packet.
        It does this by instantiating a Packet object with the relevant
        data of the incoming packet.
        """
        # pck = Packet(data)

    def test_read(self):
        # TEST READ
        # TODO
        self.logger.log(2, "Starting test dataread")
        msg, addr = self.sock.recvfrom(1024)
        print(msg)

    def test_write(self):
        # TEST WRITE
        self.logger.log(2, "Starting test datawrite")
        self.sock.connect((self.TEST_IP, self.TEST_PORT))
        self.sock.sendall(bytes("wow", "utf-8"))


if __name__ == '__main__':
    # JUST DEBUGGAN
    import oshit
    t = Transport(oshit.oSHIT())
