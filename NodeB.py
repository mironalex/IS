import socket
from Crypto.Cipher import AES


PADDING = '_'
BLOCK_SIZE = 16
MODE = ''
KM_ADDRESS = '127.0.0.1'
B_ADDRESS = '127.0.0.1'
KM_PORT = 4343
B_PORT = 4344

KEY3 = '3'


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


# start server

server = socket.socket()
server.bind((B_ADDRESS, B_PORT))
server.listen(1)

# wait for mode message from node A
client, address = server.accept()
MODE = bytes.decode(client.recv(3))


