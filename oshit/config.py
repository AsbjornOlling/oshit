# standard imports
import argparse
import collections  # for abstract base classes
import os

# external imports
import configparser


class Config(collections.MutableMapping):
    """ Class that reads and holds configuration.
    Uses argparser to read cli options,
    and configparser to read from .ini file.
    Inherits from dict, so config values kan be fetched
    with a simple: config["key"].
    """
    default = {"send": False,
               "recv": False,
               "introducer": "127.0.0.1:6564",
               "file": "./upfile.txt",
               "output": "./downfile.txt",
               "crypto": "aes",
               "password": "ChangeMe",
               "loglevel": 1,
               "localport": 1423
               }  # defaults must be complete

    def __init__(self, oSHIT):
        # inherit dictionary
        super(Config, self).__init__()
        self.store = dict()
        self.update(dict())  # use the free update to set keys

        # utility imports
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger

        # read config from cli and file
        self.cli = self.read_cli()
        self.cfile = self.read_configfile("config.ini")

        self.fix_loglevel()  # quickfix :^)

        # combine the three sources
        self.store = self.make_dict()

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
                            type=int, choices=list(range(0, 4)),
                            help="Choose a loglevel between 1 and 3",
                            metavar='[0,3]')

        parser.add_argument("-lp", "--localport",
                            type=int, choices=list(range(1, 65535)),
                            help="Choose a port between 1 and 65534",
                            metavar='[1,65534]')
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
        configdict = {}
        for option in self.default.keys():
            # 1: command line args
            value = getattr(self.cli, option)

            # 2: config file
            if value is None:
                value = self.cfile.get("oSHIT", option,
                                       # 3: defaults
                                       fallback=self.default[option])
            # put into dict
            configdict[option] = value
            self.logger.log(2, "Option " + option
                            + " set to value: " + str(value))
        self.check_errors(configdict)  # quick error check
        return configdict

    def fix_loglevel(self):
        """ Quickfix for the log level before applying config """
        clilog = getattr(self.cli, "loglevel")
        filelog = self.cfile.get("oSHIT", "loglevel", fallback=None)
        deflog = self.default["loglevel"]
        newlevel = clilog if clilog else filelog if filelog else deflog
        self.logger.set_loglevel(newlevel)

    def check_errors(self, configdict):
        """ Handle impossible configurations """
        if configdict["send"] == configdict["recv"]:  # NOT XOR
            self.logger.log(0, "Choose either send OR recv")
            quit()
        if configdict["send"]:
            if not os.path.exists(configdict["file"]):
                self.logger.log(0, "Choose a send file that exists")
                quit()
        else:
            if os.path.exists(configdict["output"]):
                self.logger.log(0, "Choose a output file that dosn't exists")

    # These last methods are only in place to let Config behave as a dict
    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
