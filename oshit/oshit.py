#!/usr/bin/env python

import logger
import transport
import crypto
import packet
import filehandler
import config


class oSHIT:
    def __init__(self):
        # internal utilities
        self.config = config.Config(self)
        loglevel = 2  # TODO: loglevel in config.py
        self.logger = logger.Logger(self, loglevel)

        self.transport = transport.Transport(self)
        self.crypto = crypto.Crypto(self)
        self.packet = packet.Packet(self)
        self.filehandler = filehandler.Filehandler(self)


if __name__ == '__main__':
    app = oSHIT()
