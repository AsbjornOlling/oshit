#!/usr/bin/env python

import argparse
import configparser


class Config:
    def __init__(self, oSHIT):
        # Gets run arguments and generate --help
        usage = "%(prog)s [--send OR --revc] [-f file] [-c crypto] ..."
        desc = "A simple UDP Holepunching file Transfer program"
        parser = argparse.ArgumentParser(prog="oshit",
                                         usage=usage,
                                         description=desc)
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-s",
                           "--send",
                           action="store_true")
        group.add_argument("-r",
                           "--recv",
                           action="store_true")
        parser.add_argument("-c", "--crypto",
                            type=str,
                            help="crypto-type")
        parser.add_argument("-f", "--file",
                            type=str,
                            help="/path/to/file")
        parser.add_argument("-o", "--output",
                            type=str,
                            help="/path/to/outputfile")
        parser.add_argument("-i",
                            "--introducer",
                            type=str,
                            help="introducer server address")
        parser.add_argument("-p",
                            "--password",
                            type=str,
                            help="passphrase")
        parser.add_argument("-l",
                            "--log",
                            type=int,
                            choices=list(range(0, 4)))
        args = parser.parse_args()

        # Read config file if argument isnt set
        config = configparser.RawConfigParser()
        config.read('config.ini')

        # Sets introducer
        if args.introducer:
            self.introducer_info = args.introducer.split(':')
        else:
            self.introducer_info = [config.get("INTRUDUCER",
                                               "serverip",
                                               fallback="127.0.0.1"),
                                    config.get("INTRUDUCER",
                                               "serverport",
                                               fallback="6564")]

        # Sets crypto
        if args.crypto is not None:
            self.crypto = args.crypto
        else:
            self.crypto = config.get("ARGUMENTS",
                                     "crypto",
                                     fallback="AES")

        # Sets file
        if args.file is not None:
            self.file = args.file
        else:
            self.file = config.get("ARGUMENTS",
                                   "file",
                                   fallback="./test")

        # Sets outputfile
        if args.output is not None:
            self.output = args.output
        else:
            self.output = config.get("ARGUMENTS",
                                     "output",
                                     fallback="file")

        # Sets password
        if args.password is not None:
            self.password = args.password
        else:
            self.password = config.get("ARGUMENTS",
                                       "password",
                                       fallback="ChangeMeAlso")

        # Sets log level
        if args.log is not None:
            self.log = args.log
        else:
            self.log = config.get("ARGUMENTS",
                                  "loglevel",
                                  fallback="0")

        # Sets lanport
        self.port = config.get("CONNECTION",
                               "lanport",
                               fallback="6668")

        # Prints for test
        print(self.introducer_info)
        print(self.crypto)
        print(self.file)
        print(self.output)
        print(self.password)
        print(self.log)
        print(self.port)

        if args.send:
            print("Call send method in Transfer class")
        elif args.recv:
            print("Call recive method in Transfer class")
        else:
            print("You have to be either sender or reciver")
