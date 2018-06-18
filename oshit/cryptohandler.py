# Standard imports
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random


class CryptoHandler:
    def __init__(self, oSHIT):
        # general utility imports
        self.oSHIT = oSHIT
        self.config = oSHIT.config
        self.logger = oSHIT.logger
        self.logger.log(2, "Initializing crypto object.")

        self.rsa_random = Random.new().read
        self.key = RSA.generate(1024, self.rsa_random)

        self.aeskey = self.genaeskey()

    def genrsakey(self):
        """
        Generates a RSA key object
        """
        publickey = self.key.publickey()
        return publickey

    def rsa_encrypt(self, publickey, data):
        """
        Used to RSA encrypt data.
        Takes publickey and data to encrypt as arguments.
        """
        encrypteddata = publickey.encrypt(data, 64)
        return encrypteddata

    def rsa_decrypt(self, data):
        """
        Decrypt RSA encrypted data with own private RSA key.
        Takes encrypted data to decrypt as argument
        """
        decrypteddata = self.key.decrypt(data)
        return decrypteddata

    def genaeskey(self):
        """
        Generates a AES key object.
        Is used by the aeskey field in the constructor.
        """
        aes_key = Random.new().read(32)
        return aes_key

    def aes_encrypt(self, data):
        """
        Used to AES encrypt data.
        Takes data to encrypt as a argument.
        Uses the aeskey field in the counstructor to encrypt.
        """
        aes_cipher = AES.new(self.aeskey)
        encrypted_data = aes_cipher.encrypt(data)
        return encrypted_data

    def aes_decrypt(self, data):
        """
        Used to AES decrypt data.
        Takes encrypted data as a argument.
        Uses the aeskey field in the constructor to decrypt.
        """
        aes_cipher = AES.new(self.aeskey)
        decrypted_data = aes_cipher.decrypt(data)
        return decrypted_data
