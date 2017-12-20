import socket
from Crypto.Cipher import AES
from Crypto import Random


PORT = 4343
PADDING = '_'
BLOCK_SIZE = 16

key1 = "1"
key2 = "2"
key3 = "3"


def pad(x):
    return x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * PADDING


def AESencrypt(plaintext, key):
    key = pad(key)
    plaintext = pad(plaintext)
    cipher = AES.new(key)
    encryptedtext = cipher.encrypt(plaintext)
    return encryptedtext


# start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', PORT))
server.listen(1)
print("Server is running.")

while True:
    client, address = server.accept()
    print(str(address) + "connected.")
    data = client.recv(10).decode()
    encryptedkey = b'nothing'

    if data == "ECB":
        encryptedkey = AESencrypt(key1, key3)

    elif data == "CFB":
        encryptedkey = AESencrypt(key2, key3)

    client.send(encryptedkey)
    client.close()
