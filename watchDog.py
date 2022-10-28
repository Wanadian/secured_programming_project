#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import socket
import sys
import time

from action import createdSharedMemory, createTubes, fillSharedMemory
from primaryServer import primaryServerBehavior
from secondaryServer import secondaryServerBehavior


def launchWatchDog():
    host = '127.0.0.1'
    primaryServerPort = 1111
    secondaryServerPort = 2222

    pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
    pathTube2 = "/tmp/tubenommesecondprincipal.fifo"

    name = "leclerc"
    create = True
    size = 10

    sharedMemory = createdSharedMemory(name, create, size)
    createTubes(pathTube1, pathTube2)

    launchPrimaryServer(sharedMemory.name, pathTube1, pathTube2, host, primaryServerPort)
    launchSecondaryServer(sharedMemory.name, pathTube1, pathTube2, host, secondaryServerPort)

    # os.wait()
    time.sleep(5)

    print("WD> destroying shared memory\n")
    sharedMemory.close()
    sharedMemory.unlink()
    print("WD> destroying tubes\n")
    os.unlink(pathTube1)
    os.unlink(pathTube2)
    sys.exit(0)


def launchPrimaryServer(sharedMemoryName, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("WD> fork impossible\n")
        os.abort()
    elif newPid == 0:
        linkToWatchDog(host, port)
        primaryServerBehavior(sharedMemoryName, pathTube1, pathTube2)
        sys.exit(0)
    else:
        openWatchDogConnection(host, port)


def launchSecondaryServer(sharedMemoryName, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("WD> fork impossible\n")
        os.abort()
    elif newPid == 0:
        linkToWatchDog(host, port)
        secondaryServerBehavior(sharedMemoryName, pathTube1, pathTube2)
        sys.exit(0)
    else:
        openWatchDogConnection(host, port)


def openWatchDogConnection(host, port):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        mySocket.bind((host, port))
    except socket.error:
        print('WD> Impossible d\'établir la liaison du socket\n')
        sys.exit()

    while True:
        print('WD> Pret\n')
        mySocket.listen(2)

        connexion, address = mySocket.accept()
        print('WD> Connexion établie avec un server\n')

        connexion.send(bytes(' Are you alive ?', 'UTF-8'))
        while True:
            msgClientraw = connexion.recv(1024)
            msgClient = msgClientraw.decode('UTF-8')
            print('Server> ' + msgClient + "\n")
            if msgClient.upper() == "FIN":
                break
            msgServeur = bytes('WD> Connexion ok', 'UTF-8')
            connexion.send(msgServeur)
            time.sleep(2)

        connexion.send(bytes('WD> Fin de connexion !', 'UTF-8'))
        print('WD> Connexion interrompue.\n')
        connexion.close()
        break

    mySocket.close()
    del mySocket


def linkToWatchDog(host, port):
    time.sleep(2)
    attempt = 0
    cpt = 0
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while attempt < 5:
        try:
            attempt += 1
            mySocket.connect((host, port))
            break
        except socket.error:
            print("Serveur> Connexion au watchdog impossible\n")
            if attempt >= 5:
                sys.exit()
            time.sleep(1)
    print("Server> Connexion établie avec le watchdog\n")

    msgServeurraw = mySocket.recv(1024)
    msgServeur = msgServeurraw.decode('UTF-8')

    while True:
        if msgServeur.upper() == "FIN":
            break
        print("WD>" + msgServeur + "\n")

        if (cpt < 3):
            msgClient = bytes('Still Alive !', 'UTF-8')
            cpt += 1
            mySocket.send(msgClient)
            time.sleep(2)
        else:
            msgClient = bytes('FIN', 'UTF-8')
            mySocket.send(msgClient)
            break
    # while True:
    #     print('Serveur prêt, en attente de requêtes sur {}:{}...'.format(host, port))
    #     mySocket.listen(5)
    #
    #     connexion, adresse = mySocket.accept()
    #     print('Client connecté, adresse IP %s, port %s' % (adresse[0], adresse[1]))
    #     print('Tapez le mot FIN pour terminer.')
    #
    #     connexion.send(bytes(
    #         'Vous etes connecte au serveur de test. Envoyez vos messages (sur une ligne) ou le mot FIN pour terminer.',
    #         'UTF-8'))
    #
    #     while True:
    #         msgClientraw = connexion.recv(1024)
    #         msgClient = msgClientraw.decode('UTF-8')
    #         print('Client>', msgClient)
    #         if msgClient.upper() == 'FIN' or msgClient == '':
    #             break
    #         msgServeur = bytes(input('Serveur> '), 'UTF-8')
    #         connexion.send(msgServeur)
    #
    #     connexion.send(bytes('Fin de connexion !', 'UTF-8'))
    #     print('Connexion interrompue.')
    #     connexion.close()
    #
    #     ch = input('<R>ecommencer <T>erminer ? ')
    #     if ch.upper() == 'T':
    #         break

    print("Server> Connexion interrompue.\n")
    time.sleep(2)
    mySocket.close()
    del mySocket
