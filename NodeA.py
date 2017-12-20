import socket
from Crypto.Cipher import AES


PADDING = '_'
BLOCK_SIZE = 16


def pad(x):
    return x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * PADDING


def AESencrypt(plaintext, key):
    key = pad(key)
    plaintext = pad(plaintext)
    cipher = AES.new(key)
    encryptedtext = cipher.encrypt(plaintext)
    return encryptedtext


def AESdecrypt(encryptedtext, key):
    key = pad(key)
    cipher = AES.new(key)
    return cipher.decrypt(encryptedtext)

