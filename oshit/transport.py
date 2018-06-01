# utility imports
import socket

# python debugger
import pdb

# Transport
# Implementation of the oSHIT protocol
# for tcp-like flow control and error control 
# over udp.
class Transport():
    LOCAL_IP = "0.0.0.0"
    LOCAL_PORT = 4222
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

        ##
        ## DEBUGGING SHIT from here on
        ## Beware - this is barely code.
        ##
        # TEST CONNECT 
        self.logger.log(2, "Connecting to " + self.TEST_IP + ":" + str(self.TEST_PORT))
        self.sock.connect((self.TEST_IP, self.TEST_PORT))

        # test send
        print("SENDING")
        self.sock.sendto(bytes("HELLO WORD", "utf-8"),
                         (self.TEST_IP, self.TEST_PORT))

        # test receive
        print("RECEIVING")
        while True:
            message = self.sock.recv(5)  # max size of udp packet
            print("GITPACKET")
            print(message)


    def create_socket(self):
        """ Create a UDP socket to the TEST IP"""
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    
    def get_timeout(self):
        """ TODO
        Calculates the optimal timeout in milis,
        based on a moving average of the round trip time so far.
        """
        return 1000


if __name__ == '__main__':
    # JUST DEBUGGAN
    t = Transport()
