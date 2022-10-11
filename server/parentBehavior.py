#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os, socket, sys


def parentBehavior(pathTube1, pathTube2):
    communicationChild(pathTube1, pathTube2)
    communicationWatchDog()

def communicationChild(pathTube1, pathTube2):
    try:
        print('Ouverture du tube1 en écriture...')
        fifo1 = open(pathTube1, "w")
        print('Ouverture du tube2 en lecture...')
        fifo2 = open(pathTube2, "r")

        for i in range(3):
            print('Processus principal prêt pour échanger des messages...')
            print('Écriture dans le tube1...')
            fifo1.write("Message du processus principal!\n")
            fifo1.flush()
            print('Processus principal en attente de réception de messages...')
            line = fifo2.readline()
            print("Message recu : " + line)

        print('Fermeture du tube1...')
        fifo1.close()
        print('Fermeture du tube2...')
        fifo2.close()
        print('Destruction des tubes...')
        print('Destruction des tubes...')
        os.unlink(pathTube1)
        os.unlink(pathTube2)
        os.execlp("ipcs", "ipcs", "-m")
    except OSError as error:
        print("Error:", error)

def communicationWatchDog():
    hostWatchDog = '127.0.0.1'
    portWatchDog = 2222
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.bind((hostWatchDog, portWatchDog))
    except socket.error:
        print('\nImpossible d\'établir la liaison du socket à l\'adresse choisie ({}:{}) !\n'.format(hostWatchDog, portWatchDog))
        sys.exit()
    while True:
        print('Serveur prêt, en attente de requêtes sur {}:{}...'.format(hostWatchDog, portWatchDog))
        mySocket.listen(5)

        (connexion, address) = mySocket.accept()
        print('Client connecté, adresse IP %s, port %s' % (address[0], address[1]))
        print('Tapez le mot FIN pour terminer.')

        connexion.send(bytes('Connected to server','UTF-8'))
        while True:
            msgClientraw = connexion.recv(1024)
            msgClient = msgClientraw.decode('UTF-8')
            print('watch dog>', msgClient)
            if msgClient.upper() == "FIN":
                break
            msgServeur = bytes('Server> Connexion ok', 'UTF-8')
            connexion.send(msgServeur)

        connexion.send(bytes('Fin de connexion !', 'UTF-8'))
        print('Connexion interrompue.')
        connexion.close()

        ch = input('<R>ecommencer <T>erminer ? ')
        if ch.upper() == 'T':
            break

    mySocket.close()
    del mySocket
    sys.exit(0)
