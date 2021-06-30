"""
- the server will send the files and folders
"""

import os
import socket
import threading

print('[+]- Server')

# server

bind_ip = '0.0.0.0'
bind_port = 5043


def check_log_exists():
    namelogfile = 'logshipping.log'
    pathDesktop = f"{os.path.join(os.environ['USERPROFILE'], 'desktop')}"
    pathLogfile = os.path.join(pathDesktop, namelogfile) # log file path in the desktop

    if os.path.isfile(pathLogfile):
        print('existe')
    else:
        os.mkdir(pathLogfile)

check_log_exists()

def server():
    instancesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    instancesocket.bind((bind_ip, bind_port))
    instancesocket.listen(10)
    print(f'the server is open at the port: {bind_port}')

    def treatCustomer(socketClient):
        #  receive what the customer sends
        socketClient.close()

    while True:
        socketclient, addr = instancesocket.accept()
        print(f'connectend there is: {addr}')

        clienthread = threading.Thread(target=treatCustomer, args=(socketclient, ))
        clienthread.start()

# function main

if __name__ == '__main__':
    server()