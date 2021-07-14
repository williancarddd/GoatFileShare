import os
import socket
import logging
import json
import  time
import  base64
import  threading

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


    def createFolderFile(self, sPathFile, sFolderFile, sDataFile):

        if os.path.isfile(sPathFile): # se o arquivo existir
            return "This file already exist."
        else:
            if not os.path.exists(sFolderFile):
                os.makedirs(sFolderFile) # cria o path do arquivo ex: a/v/c
            else:

                with open(sPathFile, 'wb') as archive: # cria o arquivo no path indicado ex: a/v/c/fileEx.ex
                    decodedB64file = base64.b64decode(sDataFile.encode())
                    archive.write(decodedB64file)
                    archive.close()

class clientReceive(object):
    def __init__(self, port:int, ipServ: str):
        self.port = port
        self.ipServ = ipServ
        self.isrunningg = False

        #variaveis de path
        self.pathUser = os.environ['USERPROFILE']
        self.pathDesktop = os.path.join(self.pathUser, 'desktop')

        #cria log
        self.createLog()

        #  create instance socket
        #  assim que a classe for instanciada o cliente começará a rodar.

        try:
            self.instanceSocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.instanceSocketClient.connect((self.ipServ, self.port))
            self.isrunningg = True
            print('client started, ready for sending files...')
            logging.info(f'connected to server:{self.ipServ} at the door: {self.port}')


        except ConnectionRefusedError as erro:
            print('the server is not online', erro)
            logging.critical(f'unable to connect to server.')

        # handle files
        self.handlefiles = FileHandLing()

    def createLog(self):

        formatLog = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
        nameLog = os.path.join(self.pathDesktop, 'logSyncFilesClient.log')
        logging.basicConfig(filename=nameLog, level=logging.DEBUG, format=formatLog)

    def run(self):

        if self.isrunningg:

            while True:
                protocol = self.instanceSocketClient.recv(1024).decode()
                print(protocol)

                if protocol == 'SyncFilesFolders':
                    self.instanceSocketClient.send(b'okSyncFilesFolders')
                    jsonPathsObjects = self.instanceSocketClient.recv(80192).decode() # recebe um json com os nomes dos arq
                    jsonDataObjects = self.instanceSocketClient.recv(98000000).decode() # json com os dados dos arquivos
                    print(jsonPathsObjects)
                    print(len(jsonDataObjects))
                    dictJsonServerData = json.loads(jsonPathsObjects)
                    listData = json.loads(jsonDataObjects)

                    for indiceFolder, namePath  in enumerate(dictJsonServerData["ListWalRelativeFiles"]):
                        nameFolder = dictJsonServerData["ListNameFolders"][indiceFolder]
                        dataFile = listData[indiceFolder]
                        teste = threading.Thread(target=self.handlefiles.createFolderFile, args=(namePath, nameFolder,dataFile ))
                        teste.run()

        else:
            print('RUN: Unable to run the client.')


if __name__ == '__main__':

     instanc = clientReceive(5043, '127.0.0.1')
     instanc.run()
