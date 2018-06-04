# library imports
import argparse
import configparser


class Config(dict):
    """ Class that reads and holds configuration.
    Uses argparser to read cli options,
    and configparser to read from .ini file.
    Inherits from dict, so config values kan be fetched,
    with simply Config["key"].
    """
    default = {"send": False,
               "recv": False,
               "introducer": "127.0.0.1:6564",
               "file": "./upfile.txt",
               "output": "./downfile.txt",
               "crypto": "aes",
               "password": "ChangeMe",
               "loglevel": 2
               }  # defaults must be complete

    def __init__(self, oSHIT):
        # inherit dictionary
        super(Config, self).__init__(self)

        # utility imports
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger

        # read config from cli and file
        self.cli = self.read_cli()
        self.cfile = self.read_configfile("config.ini")

        # combine the three sources
        self = self.make_dict()

    def read_cli(self):
        """ Use argparser to read options from command line
        Also generates --help, and provides interactive logic.
        """
        # help info
        usage = "%(prog)s [--send OR --recv] [-f file] [-c crypto] ..."
        desc = "A simple UDP holepunching file transfer program"

        # init argparser
        parser = argparse.ArgumentParser(prog="oshit",
                                         usage=usage,
                                         description=desc)

        # send OR receive
        sendreceive = parser.add_mutually_exclusive_group()
        sendreceive.add_argument("-s", "--send",
                                 action="store_true")
        sendreceive.add_argument("-r", "--recv",
                                 action="store_true")
        # TODO conditionally mandatory
        parser.add_argument("-f", "--file",
                            type=str, help="/path/to/file")
        # optional arguments
        parser.add_argument("-c", "--crypto",
                            type=str, choices=["aes", "none"])

        parser.add_argument("-o", "--output",
                            type=str, help="/path/to/outputfile")

        parser.add_argument("-i", "--introducer",
                            type=str, help="introducer server <host:port>")

        parser.add_argument("-p", "--password",
                            type=str, help="password")

        parser.add_argument("-l", "--loglevel",
                            type=int, choices=list(range(0, 4)))
        # return Namespace obj
        return parser.parse_args()

    def read_configfile(self, cfilepath):
        """ Read a given config file """
        cparser = configparser.RawConfigParser()
        cparser.read(cfilepath)
        return cparser

    def make_dict(self):
        """ Assemble final cofig dict.
        This method combines sources by priority
        1. CLI arguments
        2. Config file
        3. Defaults dict
        """
        optionsdict = {}
        for option in self.default.keys():
            # 1: command line args
            value = getattr(self.cli, option)

            # 2: config file
            if value is None:
                value = self.cfile.get("oSHIT", option,
                                       # 3: defaults
                                       fallback=self.default[option])
            # put into dict
            optionsdict[option] = value
            self.logger.log(2, "Option " + option
                            + " set to value: " + str(value))
        return optionsdict
