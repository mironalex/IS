import socket
from Crypto.Cipher import AES


PADDING = '_'
BLOCK_SIZE = 16
MODE = 'CFB'.encode('utf-8')
KM_ADDRESS = '127.0.0.1'
B_ADDRESS = '127.0.0.1'
KM_PORT = 4343
B_PORT = 4344
FILE_PATH = "./testfile"

KEY3 = '3'
IV = '1234567890123456'


def pad(x):
    if len(x) % BLOCK_SIZE != 0:
        return x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * PADDING
    return x


def byte_xor(byte_array1, byte_array2):
    result = bytearray()
    for byte1, byte2 in zip(byte_array1, byte_array2):
        result.append(ord(byte1) ^ ord(byte2))
    return bytes(result)


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


if __name__ == "__main__":
    # tell B the operating mode
    conn_to_b = socket.socket()
    conn_to_b.connect((B_ADDRESS, B_PORT))
    conn_to_b.send(MODE)
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
        with open(FILE_PATH, "rb+") as f:
            if MODE == 'ECB':
                block = f.read(BLOCK_SIZE)
                while len(block) != 0:
                    encrypted_block = AESencrypt(block, key)
                    conn_to_b.send(encrypted_block)
                    block = f.read(BLOCK_SIZE)

            elif MODE == 'CFB':
                block = f.read(BLOCK_SIZE)
                previous_encrypted_block = IV
                while len(block) != 0:
                    cipher_block = AESencrypt(previous_encrypted_block, key)
                    encrypted_block = byte_xor(block, cipher_block)
                    conn_to_b.send(encrypted_block)
                    previous_encrypted_block = encrypted_block
                    block = f.read(BLOCK_SIZE)

    conn_to_b.close()
