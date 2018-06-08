# app imports
import crypto

# XXX: None of this is actually implemented properly
# treat this whole thing as a shitty skeleton of good things to come


class Packet():
    """ Object representing one packet.
    Has fields to represent flags in the packet header,
    method to encrypt / decrypt the packet.
    This class should never be used directly, instantiate either
    InPacket or OutPacket.
    """
    def __init__(self, data):
        # TODO flags
        self.ACK = False
        self.NACK = False
        self.SEQ = 0
        self.EOF = False
        self.payload = bytes(1456)

    def get_bytes(self):
        """ Get unencrypted bytes of entire packet
        Header, payload and all.
        """
        pass


class InPacket(Packet):
    """ Packet object for incoming data.
    Has the appropriate constructor for decryption etc.
    Is instantiated in transport.rx.
    """
    def __init__(self, data):
        super(InPacket, self).__init__()
        # decrypt
        # parse header
        # read payload
        # ? checksum
        pass


class OutPacket(Packet):
    """ Packet object for outgoing data.
    Has the appropriate constructor for encryption, etc.
    Is instantiated in the application layer (oSHIT)
    """
    def __init__(self, data, eof=False):
        super(InPacket, self).__init__()
        # make header
        # read payload
        # ? checksum
        # encrypt
        pass
