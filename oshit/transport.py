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
        try:
            self.sock.connect((self.TEST_IP, self.TEST_PORT))
            self.logger.log(2, "Successfully connected.")
        except:
            self.logger.log(2, "Failed connect to" + self.TEST_IP + ":" + str(self.TEST_PORT))

        # TEST SEND
        message = "HELLO WORLD"
        self.logger.log(2, "Test-sending " + message)
        self.sock.sendto(bytes(message, "utf-8"),
                         (self.TEST_IP, self.TEST_PORT))

        # test receive
        chunk = 5  # TODO set to max size of udp packet
        self.logger.log(2, "Entering infinite " + str(chunk) + " byte print loop")
        while True:
            message = self.sock.recv(chunk)
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
