import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

if __name__ == "__main__":
    while True:
        clientsocket, address = s.accept()
        print(f"connection from {address}")
        msg = "Welcome to the server!"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg, "utf-8"))
