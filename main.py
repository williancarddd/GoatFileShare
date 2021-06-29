import os
import socket
import threading

print('[+]- Server')
# server

bind_ip = '0.0.0.0'
bind_port = 5043


def server():
    instancesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    instancesocket.bind((bind_ip, bind_port))
    instancesocket.listen(10)

    print(f'the server is open at the port: {bind_port}')

    def treatCustomer(socketClient):
        #  receive what the customer sends
        socketClient.sendall(b'HTTP/1.0 200 OK\r\nContent-Length: 11\r\nContent-Type: text/html; charset=UTF-8\r\n\r\nHello World\r\n')
        data = socketClient.recv(8192)
        print(f'received {data} ')
        socketClient.close()

    while True:
        socketclient , addr = instancesocket.accept()
        print(f'Conectado a {addr}')
        clienthread = threading.Thread(target=treatCustomer, args=(socketclient, ))
        clienthread.start()

# function main

if __name__ == '__main__':
    server()