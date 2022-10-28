#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import socket
import sys
import time

from action import createdSharedMemory, createTubes
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

    os.wait()

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
    watchDogSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        watchDogSocket.bind((host, port))
    except socket.error:
        print('WD> Impossible d\'établir la liaison du socket\n')
        sys.exit()

    print('WD> Pret\n')
    watchDogSocket.listen(2)

    connexion, address = watchDogSocket.accept()
    print('WD> Connexion établie avec un server\n')

    while True:
        connexion.send(bytes('Are you alive ?', 'UTF-8'))
        messageRecieved = connexion.recv(1024).decode('UTF-8')
        print('Server> ' + messageRecieved + "\n")
        if messageRecieved.upper() == "FIN":
            break
        time.sleep(2)

    print('WD> Connexion interrompue avec le server.\n')
    connexion.close()

    watchDogSocket.close()
    del watchDogSocket


def linkToWatchDog(host, port):
    time.sleep(2)
    attempt = 0
    cpt = 0
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while attempt < 5:
        try:
            attempt += 1
            serverSocket.connect((host, port))
            break
        except socket.error:
            print("Serveur> Connexion au watchdog impossible\n")
            if attempt >= 5:
                sys.exit()
            time.sleep(1)
    print("Server> Connexion établie avec le watchdog\n")

    while True:
        messageRecieved = serverSocket.recv(1024).decode('UTF-8')
        print("WD> " + messageRecieved + "\n")

        if cpt < 5:
            cpt += 1
            serverSocket.send(bytes('Still alive !', 'UTF-8'))
        else:
            serverSocket.send(bytes('FIN', 'UTF-8'))
            break

    serverSocket.close()
    del serverSocket
