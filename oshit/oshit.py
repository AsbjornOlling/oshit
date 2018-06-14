#!/usr/bin/env python

import logger
import transport
import filehandler
import config

from logic import testlogic

class oSHIT:
    def __init__(self):
        # internal utilities
        # set temp loglevel, while loading config
        temploglevel = config.Config.default["loglevel"]
        self.logger = logger.Logger(self, temploglevel)
        self.config = config.Config(self)

        # self.transport = transport.Transport(self)
        # self.filehandler = filehandler.Filehandler(self)

        tl = testlogic.TestReceiveLogic(self, CONNECT_ADDR=("", 1), oSHIT=self)


if __name__ == '__main__':
    app = oSHIT()
