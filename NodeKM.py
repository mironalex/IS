import socket


PORT = 4343

key1 = "1"
key2 = "2"
key3 = "3"

# start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', PORT))
server.listen(1)
print("Server is running.")

while True:
    client, address = server.accept()
    print(str(address) + "connected.")

    data = client.recv(10).decode()

    if data == "ECB":
        pass

    elif data == "CFB":
        pass

    else:
        client.close()
        continue

