# utility imports
import socket


class Transport():
    """ Implementation of the oSHIT protocol
    for tcp-like flow control and error control
    over udp.
    """
    # info for local socket
    LOCAL_IP = ""
    LOCAL_PORT = 4222

    # connect to this one
    TEST_IP = "127.0.0.1"
    TEST_PORT = 5555

    def __init__(self, oSHIT):
        # general utility imports
        self.oSHIT = oSHIT
        self.config = oSHIT.config
        self.logger = oSHIT.logger
        self.logger.log(2, "Initializing transport object.")

        # queue of packets
        self.packets = []

        # create socket
        self.sock = self.create_socket()

        # TEST READ
        self.logger.log(2, "Starting test dataread")
        msg, addr = self.sock.recvfrom(1024)
        print(msg)

        # TEST WRITE
        self.logger.log(2, "Starting test datawrite")
        self.sock.connect((self.TEST_IP, self.TEST_PORT))
        self.sock.sendall(bytes("wow", "utf-8"))

    def create_socket(self):
        """ Create a UDP socket to the TEST IP"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind((self.LOCAL_IP, self.LOCAL_PORT))
        return sock

    def get_timeout(self):
        """ TODO
        Calculates the optimal timeout in milis,
        based on a moving average of the round trip time so far.
        """
        return 1000


if __name__ == '__main__':
    # JUST DEBUGGAN
    import oshit
    t = Transport(oshit.oSHIT())
