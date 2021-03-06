
class Logger():
    """ Logger
    Simple logging utility
    """
    def __init__(self, oSHIT, loglevel):
        self.oSHIT = oSHIT
        self.set_loglevel(loglevel)
        self.logfile = None

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

            if self.logfile:
                self.logfile.write(logstring + "\n")
            print(output)

    def set_loglevel(self, loglevel):
        self.loglevel = int(loglevel)

    def open_logfile(self, logfilepath):
        self.logfile = open(logfilepath, 'a')
