# Crypto specs

## Crypto types

### AES

We use AES for file encryption, the key is random generated and stored in a field:
self.aeskey.

### RSA

We use RSA to encrypt the AES key.

## Methods

Cryptohandler has 6 methods:

Generate key
Encrypt
Decrypt

Times 2 because all three methods exists for both AES and RSA
