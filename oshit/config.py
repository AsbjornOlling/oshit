#!/usr/bin/env python

import argparse


class Config:
    def __init__(self, oSHIT):
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
        parser.add_argument("-l", "--log", type=int, choices=list(range(0, 4)))
        args = parser.parse_args()

        if args.send:
            print("Call send method in Transfer class")
        elif args.recv:
            print("Call recive method in Transfer class")
        else:
            print("You have to be either sender or reciver")
