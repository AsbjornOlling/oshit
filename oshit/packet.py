# external imports
# from bitarray import bitarray

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
    HSIZE = 2     # header: 2 bytes
    PSIZE = 1456  # payload size : 1456 bytes

    def __init__(self, data, oSHIT=None):
        self.logger = oSHIT.logger

    def get_bytes(self):
        """ Get unencrypted bytes of entire packet
        Header, payload and all.
        """
        pass

    def get_payload(self):
        """ Get the packets payload as bytes object """
        return self.get_payload

    def encrypt(self):
        # TODO
        pass

    def decrypt(self):
        # TODO
        pass

    def check_fields(self):
        """ Check fields for invalid states """
        error = False

        if self.SEQ is None:
            self.logger.log(0, "Tried to create packet without seqeuence no.")
            error = True

        if self.ACK and self.NACK:
            self.logger.log(0, "Tried to create packet with ACK and NACK set.")
            error = True

        if error:
            self.logger.log(0, "Quitting because of bad packet error.")
            quit()


class InPacket(Packet):
    """ Packet object for incoming data.
    Has the appropriate constructor for decryption etc.
    Is instantiated in transport.rx.
    """
    def __init__(self, data):
        super(InPacket, self).__init__()

        # get header
        header = data[:self.HSIZE]
        # parse header
        self.SEQ = self.read_seq(header)
        self.ACK, self.NACK, self.EOF = self.read_flags(header)

        # rest of packet is payload
        self.payload = data[self.HSIZE:]

        # TODO: decryption
        # ? checksum

    def read_seq(self, header):
        """ Read sequence number from first byte of header. """
        seq = header[0]
        return seq

    def read_flags(self, header):
        """ Read protocol bit flags from header. """
        # get flag bits
        flagbyte = header[1]
        bitstring = bin(flagbyte)[2:].zfill(8)
        bitarray = [True if char == '1' else False for char in bitstring]

        # detect flags
        ack = bitarray[0]
        nack = bitarray[1]
        eof = bitarray[2]
        return (ack, nack, eof)


class OutPacket(Packet):
    """ Packet object for outgoing data.
    Has the appropriate constructor for encryption, etc.
    Is instantiated in the application layer (oSHIT)
    """
    def __init__(self, payload, seq=None, ack=False, nack=False, eof=False):
        super(InPacket, self).__init__()

        # set header fields
        self.SEQ = seq
        self.ACK = ack
        self.NACK = nack
        self.EOF = eof
        self.check_fields()

        self.payload = payload

        # TODO: encryption
        # TODO: checksum
