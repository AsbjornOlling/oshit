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
        self._file = open(self.config["file"], 'rb')

    def read_chunk(self):
        """ Use the path from config to read chunks of file.
        returns the read chunks as bytes, and EOF as a boolean.
        """
        self.eof = False
        chunk = self._file.read(self.PSIZE)
        if not chunk:
            self.eof = True
            self._file.close()
        return(chunk, self.eof)
