import os


class FileHandler():
    """ Class handling read and write to files.
    Uses default python open and read.
    """

    PSIZE = 1456

    def __init__(self, oSHIT):
        # general utility imports
        self.oSHIT = oSHIT
        self.config = oSHIT.config
        self.logger = oSHIT.logger
        self.logger.log(2, "Initializing filehandler object.")

        # Open the file
        self._readfile = open(self.config["file"], 'rb')

    def read_chunk(self):
        """ Use the path from config to read chunks of file.
        returns the read chunks as bytes, and EOF as a boolean.
        """
        try:
            eof = False
            readchunk = self._readfile.read(self.PSIZE)
            if not readchunk:
                eof = True
                self._readfile.close()
            return(readchunk, eof)
        except:
            print("Called read_chunk after EOF")

    def write_chunk(self, writedata):
        """ Takes a datachunk as argument and write it to a file.
        It appends the data if the file already exits.
        """
        mode = 'ab' if os.path.exists(self.config['output']) else 'wb'
        _writefile = open(self.config['output'], mode)
        _writefile.write(writedata)
        _writefile.close()
