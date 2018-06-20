#!/usr/bin/env python

# application imports
import logger
import config
from peerlogic import SendLogic, ReceiveLogic


class oSHIT:
    def __init__(self):
        # internal utilities
        # set temp loglevel, while loading config
        temploglevel = config.Config.default["loglevel"]
        self.logger = logger.Logger(self, temploglevel)
        self.config = config.Config(self)

        # start logic
        if self.config["send"]:
            self.logic = SendLogic(oSHIT=self)
        elif self.config["recv"]:
            self.logic = ReceiveLogic(oSHIT=self)


if __name__ == '__main__':
    app = oSHIT()
