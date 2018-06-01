
# Transport
# Implementation of the oSHIT protocol
# for tcp-like flow control and error control 
# over udp.
class Transport:
    def __init__(self, oSHIT):
        # parent object
        self.oSHIT = oSHIT
        self.config = oSHIT.config

        # init fields
        self.packets = []

        
