import os
import socket
import threading
import logging


class ServerSend(object):

    def __init__(self, port: int, ipServ: str):

        #  configurações do servidor
        self.port = port
        self.ipServ = ipServ
        self.isRunnig = False  # controle de funcionamento do servidor.

        #  variáveis de path
        self.pathUser = os.environ['USERPROFILE']
        self.pathDesktop = os.path.join(self.pathUser, 'desktop')

        # criação do arquivo de log na área de trabalho
        self.createLog()

        #  assim que a classe for instanciada o servidor começará a rodar.
        #############################################################################################
        try:

            self.instanceSocketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.instanceSocketServer.bind((self.ipServ, self.port))  # começa a rodar na porta e no servidor indicado.
            self.instanceSocketServer.listen(5)
            print(', ready for file transfer...')
            logging.info('server was started')
            self.isRunnig = True

        except Exception as Error:

            print('server survey error.', Error)
            logging.critical(Error)
        ###############################################################################################

    def treatCustomer(self, socketclient):
        # essa função deve ser passada com callback para thread
        #  essa função vai tratar tudo que vier do cliente, ou seja , todos os tipos de dados enviados.
        print('treating customer')
        print(socketclient.recv(1024))

        pass

    def createLog(self):

        formatLog = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
        nameLog = os.path.join(self.pathDesktop,'loginSyncFiles.log')

        logging.basicConfig(filename=nameLog, level=logging.DEBUG, format=formatLog)
        logging.debug('The log file has been created')

    def run(self):
        if self.isRunnig:
            while True:
                print('RUN: loop function run')
                client, addr = self.instanceSocketServer.accept() #  fica aceitando conexões.

                #  a Threading vai ficar recebendo os clientes.
                client_handler = threading.Thread(target=self.treatCustomer, args=(client,))
                client_handler.start()
        else:
            print('RUN: server was not raised.')


if __name__ == '__main__':
    instanc = ServerSend(5043, '127.0.0.1')

    instanc.run()

