import socket
from Crypto.Cipher import AES


PORT = 4343
PADDING = chr(0)
BLOCK_SIZE = 16

KEY1 = "1"
KEY2 = "2"
KEY3 = "3"


def pad(x):
    if len(x) % BLOCK_SIZE != 0:
        if isinstance(x, (bytes, bytearray)):
            x = x.decode()
        return x + ((BLOCK_SIZE - len(x) % BLOCK_SIZE) - 1) * PADDING + (chr(BLOCK_SIZE - len(x) % BLOCK_SIZE))
    return x


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
    encryptedkey = b'NA'

    if data == "ECB":
        encryptedkey = AESencrypt(KEY1, KEY3)

    elif data == "CFB":
        encryptedkey = AESencrypt(KEY2, KEY3)

    client.send(encryptedkey)
    client.close()
