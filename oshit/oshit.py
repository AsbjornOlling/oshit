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
        # set temp loglevel, while loading config
        temploglevel = 2
        self.logger = logger.Logger(self, temploglevel)
        self.config = config.Config(self)

        self.transport = transport.Transport(self)
        self.crypto = crypto.Crypto(self)
        self.packet = packet.Packet(self)
        self.filehandler = filehandler.Filehandler(self)


if __name__ == '__main__':
    app = oSHIT()
