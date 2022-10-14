#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os, socket, sys
import time
from action import createdSharedMemory, fillSharedMemory, createTubes, closeSegments
from secondaryServer import secondaryServerBehavior
from watchDog import watchDog


def createWatchDog(hostWatchDog, portWatchDog):
    newPid = os.fork()

    if newPid < 0:
        print("fork() impossible")
        os.abort()
    elif newPid == 0:
        communicationWatchDog(hostWatchDog, portWatchDog)
    else:
        watchDog(hostWatchDog, portWatchDog)


def createSecondaryServer(shareMemory, pathTube1, pathTube2):
    newPid = os.fork()

    if newPid < 0:
        print("fork() impossible")
        os.abort()
    elif newPid == 0:
        communicationSecondaryServer(pathTube1, pathTube2)
    else:
        secondaryServerBehavior(shareMemory, pathTube1, pathTube2)


def communicationSecondaryServer(pathTube1, pathTube2):
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


def communicationWatchDog(hostWatchDog, portWatchDog):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        mySocket.bind((hostWatchDog, portWatchDog))
    except socket.error:
        print('\nImpossible d\'établir la liaison du socket à l\'adresse choisie ({}:{}) -- Parent !\n'.format(hostWatchDog, portWatchDog))
        sys.exit()
    while True:
        print('Serveur prêt, en attente de requêtes sur {}:{}.. -- Parent.'.format(hostWatchDog, portWatchDog))
        mySocket.listen(5)

        connexion, address = mySocket.accept()
        print('Client connecté, adresse IP %s, port %s' % (address[0], address[1]))

        connexion.send(bytes('Connected to server','UTF-8'))
        while True:
            msgClientraw = connexion.recv(1024)
            msgClient = msgClientraw.decode('UTF-8')
            print('watch dog>', msgClient)
            if msgClient.upper() == "FIN":
                break
            msgServeur = bytes('Server> Connexion ok', 'UTF-8')
            connexion.send(msgServeur)
            time.sleep(2)

        connexion.send(bytes('Fin de connexion !', 'UTF-8'))
        print('Connexion interrompue.')
        connexion.close()
        break

    mySocket.close()
    del mySocket
    

def launchPrimaryServer():
    host = '127.0.0.1'
    port = 1111

    name = "leclerc"
    create = True
    size = 10
    data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
    pathTube2 = "/tmp/tubrm enommesecondprincipal.fifo"

    createWatchDog(host, port)
    sharedMemory = createdSharedMemory(name, create, size)
    fillSharedMemory(sharedMemory, data)
    createTubes(pathTube1, pathTube2)
    createSecondaryServer(sharedMemory, pathTube1, pathTube2)
    closeSegments(sharedMemory)


launchPrimaryServer();