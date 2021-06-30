import os
import socket


class clientReceive(object):
    def __init__(self, port:int, ipServ: str):
        self.port = port
        self.ipServ = ipServ
        self.isrunningg = False

        #  create instance socket
        #  assim que a classe for instanciada o servidor começará a rodar.
        self.instanceSocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            self.instanceSocketClient.connect((self.ipServ, self.port))
            self.isrunningg = True
            print('client started, ready for sending files...')

        except ConnectionRefusedError as erro:
            print('the server is not online', erro)


    def run(self):

            if self.isrunningg:
              while True:
                  pass
            else:
                print('RUN: Unable to run the client.')


if __name__ == '__main__':

    instanc = clientReceive(5043, '127.0.0.1')
    instanc.run()
