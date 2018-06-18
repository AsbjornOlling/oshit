#!/usr/bin/env python

import logger
import filehandler
import config
import cryptohandler


class oSHIT:
    def __init__(self):
        # internal utilities
        # set temp loglevel, while loading config
        temploglevel = config.Config.default["loglevel"]
        self.logger = logger.Logger(self, temploglevel)
        self.config = config.Config(self)

        self.cryptohandler = cryptohandler.CryptoHandler(self)
        self.filehandler = filehandler.FileHandler(self)

        # test crypto
        self.readfile = self.readfile()
        self.rsakey = self.genrsakey()
        self.rsa_encrypt = self.rsa_encrypt()
        self.aes_encrypt = self.aes_encrypt()
        self.rsa_decrypt = self.rsa_decrypt()
        self.aes_decrypt = self.aes_decrypt()
        self.filehandler.write_chunk(self.aes_decrypt)

    # Reads from the file with filehandler
    def readfile(self):
        filechunk = self.filehandler.read_chunk()
        return filechunk

    # Generates a RSA key with cryptohandler
    def genrsakey(self):
        rsakey = self.cryptohandler.genrsakey()
        return rsakey

    # Encrypts AES key with RSA testing cryptohandler
    def rsa_encrypt(self):
        rsaencryptedkey = self.cryptohandler.rsa_encrypt(self.rsakey, self.cryptohandler.aeskey)
        return rsaencryptedkey

    # AES encrypt the read data
    def aes_encrypt(self):
        aes_encrypted_data = self.cryptohandler.aes_encrypt(self.readfile[0])
        return aes_encrypted_data

    # RSA decrypts the AES key
    def rsa_decrypt(self):
        rsadecryptedkey = self.cryptohandler.rsa_decrypt(self.rsa_encrypt)
        return rsadecryptedkey

    # AES decrypts the data
    def aes_decrypt(self):
        self.cryptohandler.genaeskey = self.rsa_decrypt
        aes_decrypted_data = self.cryptohandler.aes_decrypt(self.aes_encrypt)
        print(aes_decrypted_data)
        return aes_decrypted_data


if __name__ == '__main__':
    app = oSHIT()
