#!/usr/bin/env python

# standard imports
import time
import sys

# application imports
sys.path.insert(0, '../oshit')
from oshit import oSHIT
from logic import Logic
from transport import Transport
import packet
from filehandler import FileHandler


class TestRecvPeer(Logic):
    """
    """
    def __init__(self, CONNECT_ADDR=None, LOCAL_ADDR=None, oSHIT=None):
        # parent constructor (make threads to communicate with transport)
        # also get relevant inherted objects
        super(TestRecvPeer, self).__init__(oSHIT=oSHIT)

        # make filehandler
        self.fileh = FileHandler(self.oSHIT)

        # connect to peer
        self.CONNECT_ADDR = CONNECT_ADDR
        self.LOCAL_ADDR = LOCAL_ADDR
        self.transport = self.connect()

        # start!
        self.start_threads()

    def connect(self):
        """ Make a Transport object to the given address. """
        return Transport(CONNECT_ADDR=self.CONNECT_ADDR,
                         LOCAL_ADDR=self.LOCAL_ADDR,
                         logic=self)

    def handle_incoming(self, pck):
        """ Mandatory Logic method. Handles incoming packets.
        This one writes each packet to a file using FileHandler.
        """
        self.logger.log(1, "TestRecvPeer writing received data to file.")
        data = pck.get_payload()
        self.fileh.write_chunk(data)
        if pck.EOF:
            self.logger.log(1, "TestRecvPeer got EOF. Idling.")

    def get_next_packet(self):
        """ Mandatory Logic method. Creates outgoing packets.
        This one does nothing.
        """
        self.logger.log(1, "TestRecvPeer is being asked for new packet.")
        return None


class TestSendPeer(Logic):
    # TODO me
    def __init__(self, CONNECT_ADDR=None, LOCAL_ADDR=None, oSHIT=None):
        # parent constructor (make threads to communicate with transport)
        # also get relevant inherted objects
        super(TestSendPeer, self).__init__(oSHIT=oSHIT)

        # make filehandler
        self.fileh = FileHandler(self.oSHIT)

        # connect to peer
        self.LOCAL_ADDR = LOCAL_ADDR
        self.CONNECT_ADDR = CONNECT_ADDR
        self.transport = self.connect()

        # GO GO GO
        self.start_threads()

        # dump the entire file
        self.dump_file()

    def handle_incoming(self, pck):
        """ Mandatory Logic method. Handles incoming packets.
        This one does nothing.
        """
        self.logger.log(3, "TestSendPeer received data.")

    def connect(self):
        # XXX: duplicate of TestRecvPeer.connect()
        """ Make a Transport object to the given address. """
        return Transport(CONNECT_ADDR=self.CONNECT_ADDR,
                         LOCAL_ADDR=self.LOCAL_ADDR,
                         logic=self)

    def dump_file(self):
        """ Just sends a file by dumping the entire thing, """
        eof = False
        i = 0
        while not eof:
            self.logger.log(3, "Dumping file chunk " + str(i))
            data, eof = self.fileh.read_chunk()
            pck = packet.OutPacket(data, eof=eof, oSHIT=self.oSHIT)

            self.send(pck)

        self.logger.log(1, "Hit EOF. Exiting loop.")


if __name__ == '__main__':
    app = oSHIT()
    config = app.config
    logger = app.logger
    if config["recv"]:
        logic = TestRecvPeer(CONNECT_ADDR=("127.0.0.1", 5555),
                             LOCAL_ADDR=("127.0.0.1", 6666), oSHIT=app)
    elif config["send"]:
        logic = TestSendPeer(CONNECT_ADDR=("127.0.0.1", 6666),
                             LOCAL_ADDR=("127.0.0.1", 5555), oSHIT=app)
