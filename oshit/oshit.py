#!/usr/bin/env python

import transport
import crypto
import packet
import filehandler
import config


class oSHIT:
    def __init__(self):
        self.config = config.Config(self)
        self.transport = transport.Transport(self)
        self.crypto = crypto.Crypto(self)
        self.packet = packet.Packet(self)
        self.filehandler = filehandler.Filehandler(self)


if __name__ == '__main__':
    app = oSHIT()
