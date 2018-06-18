# How crypto works in python
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

# Read some chunks from a file
readfile = open("./upfile.txt", 'rb')
readchunk = readfile.read(1456)

# Generates a AES key
aes_key = Random.new().read(32)
aes_cipher = AES.new(aes_key)

# Encrypt data with the AES key
encrypteddata = aes_cipher.encrypt(readchunk)

# Generates a RSA key
random = Random.new().read
key = RSA.generate(1024, random)
publickey = key.publickey()

# Encrypt the AES key with RSA
encrypted_key = publickey.encrypt(aes_key, 64)
# Decrypt the AES key with RSA
decryptedkey = key.decrypt(encrypted_key)

# Generates new AES cipher withe the decrypted key
sendaescipher = AES.new(decryptedkey)

# Decrypts the AES encrypted data
decrypteddata = sendaescipher.decrypt(encrypteddata)

# Write the decrypted data to a file
writefile = open("./downfile", 'wb')
writefile.write(decrypteddata)
