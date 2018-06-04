
## Logger
# Simple logging utility
class Logger():
    def __init__(self, oSHIT, loglevel):
        self.oSHIT = oSHIT

        self.loglevel = loglevel

        # TODO: add path to logfile to config object
        # when config object is functional
        logfilepath = "log"
        self.logfile = open(logfilepath, 'a')


    def log(self, loglevel, logstring):
        """ Main logging function. called from everywhere """
        # filter according to loglevel
        if self.loglevel >= loglevel:
            if loglevel == 0:
                output = "[ERROR] " + logstring
            elif loglevel == 1:
                output = "[INFO] " + logstring
            elif loglevel == 2:
                output = "[DEBUG] " + logstring
            elif loglevel == 3:
                output = "[WTF] " + logstring

            self.logfile.write(logstring + "\n")
            print(output)
