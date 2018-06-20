from connection import Connection
from packet import OutPacket
from filehandler import FileHandler


class PeerLogic:
    def __init__(self, oSHIT=None):
        self.oSHIT = oSHIT
        self.config = oSHIT.config
        self.logger = oSHIT.logger

        # make filehandler
        self.file = FileHandler(oSHIT=self.oSHIT)

    def introduce(self):
        # TODO implement me
        # - make introducer transport object
        # - get local address info
        # - make outpacket of local address info + password
        # - send packet
        # - wait for info
        # - parse info
        # - make Connection
        pass
        # return Connection

    def find_peer(self):
        """ Find and return a peer.
        Just connect immediately if direct-mode chosen,
        otherwise use an introduction server.
        """
        # just make object if direct-mode chosen
        if self.config["direct"]:
            self.logger.log(1, "Connecting in direct mode.")
            addr = self.config["direct"].split(":")
            peer = Connection((addr[0], int(addr[1])), oSHIT=self.oSHIT)
        else:  # otherwise, do the introduce
            peer = self.introduce()
        return peer


class SendLogic(PeerLogic):
    def __init__(self, oSHIT=None):
        # run parent constructor
        # inherit relevant app objects
        super(SendLogic, self).__init__(oSHIT=oSHIT)
        self.logger.log(2, "Starting SendLogic")

        # do the introduction (or not), and return peer connection
        self.recvpeer = self.find_peer()

        # start sending data
        self.send_checksum()  # 1. send file md5 checksum to recvpeer
        self.dump_file()      # 2. start dumping file

        self.logger.log(2, "Completed SendLogic.")

    def send_checksum(self):
        """ Send md5sum of the file to send """
        # make checksum packet
        md5string = self.file.gen_checksum(self.config["file"])
        md5pck = OutPacket(bytes(md5string, "utf-8"), oSHIT=self.oSHIT)

        self.logger.log(1, "Sending file checksum: " + md5string)
        self.recvpeer.send(md5pck)

    def dump_file(self):
        """ Just sends a file by dumping the entire thing, """
        eof = False
        i = 0
        while not eof:
            self.logger.log(3, "Dumping file chunk " + str(i))
            data, eof = self.file.read_chunk()
            pck = OutPacket(data, eof=eof, oSHIT=self.oSHIT)
            self.recvpeer.send(pck)
        self.logger.log(1, "Hit EOF. Exiting loop.")


class ReceiveLogic(PeerLogic):
    def __init__(self, oSHIT=None):
        # run parent constructor
        # inherit relevant app objects
        super(ReceiveLogic, self).__init__(oSHIT=oSHIT)
        self.logger.log(2, "Starting ReceiveLogic")

        self.sendpeer = self.find_peer()

        self.correctmd5 = self.get_correct_checksum()

        self.receive_file()

    def get_correct_checksum(self):
        """ Interprets the next packet as a string.
        Blindly expects the next packet to contain the checksum. """
        md5pck = self.sendpeer.get_packet()
        correctmd5 = str(md5pck.get_payload())
        self.logger.log(1, "Got MD5 checksum: " + str(correctmd5))
        return correctmd5

    def receive_file(self):
        self.logger.log(1, "Receiving file.")
        eof = False
        while not eof:
            # get packet
            pck = self.sendpeer.get_packet()

            # write payload to file
            payload = pck.get_payload()
            self.file.write_chunk(payload)

            eof = pck.EOF
        self.logger.log(1, "Transfer finished.")
