# -*- coding: utf-8 -*-
from sys import argv
import os
import socket
import threading
import logging
import shutil
import json
import  time

class FileHandLing(object):
    def __init__(self):
        self.extensionsFile = ['jpg', 'png', 'gif']


    def getFoldersFiles(self):
        # retorna uma lista com o caminho para as imagens de cada pasta.
        __listWalkRelativeFiles = []
        __listNameFolders = []
        __tupleDataFile = [] # virará uma tupla
        for root, dirs , files in os.walk('.'):
            for file in files:
                if file.split('.')[-1]  in self.extensionsFile:
                    __pathFile = os.path.join(root, file)
                    __listWalkRelativeFiles.append(__pathFile)
                    __listNameFolders.append(root)
                    __tupleDataFile.append(self.openerFile(__pathFile))

        return [{

                "ListWalRelativeFiles":__listWalkRelativeFiles,
                "ListNameFolders": __listNameFolders,
                }, __tupleDataFile]

    def openerFile(self, nameFile):
        with open(nameFile, 'rb') as archive:
            return  archive.read()


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
        # essa função deve ser passada como callback para thread da função run
        #  essa função vai tratar tudo que vier do cliente, ou seja , todos os tipos de dados enviados.
        fileHandling = FileHandLing()

        while True:

            try:

                pathData = fileHandling.getFoldersFiles()

                time.sleep(0.1) # sincroniza o envio do json em 0.1s
                socketclient.send(json.dumps(pathData[0]).encode()) # envia um objeto json para o cliente


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
