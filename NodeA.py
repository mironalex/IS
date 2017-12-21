import socket
from Crypto.Cipher import AES


PADDING = '_'
BLOCK_SIZE = 16
MODE = 'ECB'.encode('utf-8')
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


# tell B the operating mode
conn_to_b = socket.socket()
conn_to_b.connect((B_ADDRESS, B_PORT))
conn_to_b.send(b'ECB')
print('Conenction to B established')


# get corresponding key from KM
conn_to_km = socket.socket()
conn_to_km.connect((KM_ADDRESS, KM_PORT))
conn_to_km.send(bytes(MODE))
print('Connection to KM established')
encrypted_key = conn_to_km.recv(BLOCK_SIZE)
conn_to_km.close()

key = AESdecrypt(encrypted_key, KEY3)
print('decrypted key: ' + str(key))

# wait for ready message
ready_message = conn_to_b.recv(5)

if ready_message == b'READY':
    # start sending file
    pass

else:
    conn_to_b.close()
    exit()

