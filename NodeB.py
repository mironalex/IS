import socket
from Crypto.Cipher import AES


PADDING = '_'
BLOCK_SIZE = 16
MODE = ''
KM_ADDRESS = '127.0.0.1'
B_ADDRESS = '127.0.0.1'
KM_PORT = 4343
B_PORT = 4344
FILE_PATH = './outputfile'

KEY3 = '3'


def pad(x):
    if len(x) % BLOCK_SIZE != 0:
        return x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * PADDING
    return x


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

conn_to_km = socket.socket()
conn_to_km.connect((KM_ADDRESS, KM_PORT))
conn_to_km.send(bytes(MODE))
print('Key reqeuested from KM')
encrypted_key = conn_to_km.recv(BLOCK_SIZE)
conn_to_km.close()

key = AESdecrypt(encrypted_key, KEY3)

with open(FILE_PATH, "wb+") as f:
    client.send(b'READY')
    if MODE == 'ECB':
        encrypted_block = client.recv(BLOCK_SIZE)
        while len(encrypted_block) != 0:
            decrypted_block = AESdecrypt(encrypted_block, key)
            f.write(decrypted_block)
            encrypted_block = client.recv(BLOCK_SIZE)

    if MODE == 'CFB':
        pass

server.close()


