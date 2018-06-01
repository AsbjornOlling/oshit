
import socket

# Transport
# Implementation of the oSHIT protocol
# for tcp-like flow control and error control 
# over udp.
class Transport():
    TEST_IP = "localhost"
    TEST_PORT = 4222

    def __init__(self):
        # parent object
        # self.oSHIT = oSHIT
        # self.config = oSHIT.config

        # queue of packets
        self.packets = []

        # create socket
        self.sock = self.create_socket()

        # test send
        print("SENDING")
        self.sock.sendto(bytes("HELLO WORD", "utf-8"),
                         (self.TEST_IP, self.TEST_PORT))

    def create_socket(self):
        """ Create a UDP socket to the TEST IP"""
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    
    def get_timeout(self):
        """ TODO
        Calculates the optimal timeout in milis,
        based on a moving average of the round trip time so far.
        """
        return 1000


if __name__ is '__main__':
    # JUST DEBUGGAN
    t = Transport()
