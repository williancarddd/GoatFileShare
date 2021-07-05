# -*- coding: utf-8 -*-
from sys import argv
import os
import socket
import threading
import logging
import shutil
import json

class FileHandLing(object):
    def __init__(self):
        self.extensionsFile = ['jpg', 'png', 'gif']

    def getFoldersFiles(self):
        # retorna uma lista com o caminho para as imagens de cada pasta.
        __listWalkRelativeFiles = []
        __listNameFolders = []
        for root, dirs , files in os.walk('.'):
            for file in files:
                if file.split('.')[-1]  in self.extensionsFile:
                    __listWalkRelativeFiles.append(os.path.join(root, file))
                    __listNameFolders.append(root)
        return {"ListWalRelativeFiles": __listWalkRelativeFiles, "ListNameFolders": __listNameFolders}

class ServerSend(object):

    def __init__(self, port: int, ipServ: str):

        #  configurações do servidor
        self.port = port
        self.ipServ = ipServ
        self.isRunnig = False  # controle de funcionamento do servidor.

        #  variáveis de path
        self.pathUser = os.environ['USERPROFILE']
        self.pathDesktop = os.path.join(self.pathUser, 'desktop')
        self.pathAppData = os.environ['APPDATA']
        self.PathlocationThisFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), argv[0])

        # criação do arquivo de log na área de trabalho
        self.createLog()

        # tratamento de erro na criação, ligamento e listamento do socket.
        try:
            #  assim que a classe for instanciada o servidor começará a rodar.

            self.instanceSocketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.instanceSocketServer.bind((self.ipServ, self.port))  # começa a rodar na porta e no servidor indicado.
            self.instanceSocketServer.listen(5)
            print(' ready for file transfer...')
            logging.info('server was started')
            self.isRunnig = True

        except Exception as Error:

            print('server survey error.', Error)
            logging.critical(Error)


    def startWithSystem(self):
        pass

    def createLog(self):

        formatLog = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
        nameLog = os.path.join(self.pathDesktop, 'logSyncFilesServer.log')
        logging.basicConfig(filename=nameLog, level=logging.DEBUG, format=formatLog)


    def treatCustomer(self, socketclient):
        # essa função deve ser passada com callback para thread
        #  essa função vai tratar tudo que vier do cliente, ou seja , todos os tipos de dados enviados.
        fileHandling = FileHandLing()
        while True:

            try:
                pathData = fileHandling.getFoldersFiles()
                socketclient.send(json.dumps(pathData).encode()) # envia um objeto json para o client

            except ConnectionResetError as erro:
                print('the customer has disconnected',erro)
                logging.critical(f'the customer has disconnected {erro}')
                break

    def run(self):
        if self.isRunnig:
            while True:
                print('RUN: loop function run')

                client, addr = self.instanceSocketServer.accept()  # fica aceitando conexões.
                print(f'\n\nRUN:got connected {addr}')

                #  a Threading vai ficar recebendo os clientes.
                client_handler = threading.Thread(target=self.treatCustomer, args=(client, ))
                client_handler.start()
        else:
            print('RUN: server was not raised.')


if __name__ == '__main__':
     instanc = ServerSend(5043, '127.0.0.1')
     instanc.run()
