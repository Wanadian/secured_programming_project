#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import random
import signal
import socket
import sys
import time
from threading import Thread

from action import createdSharedMemory, createTubes, freeCommunicationSystem, raiseTimeoutError, terminateChildren
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

    freeCommunicationSystem(name, pathTube1, pathTube2)

    sharedMemory = createdSharedMemory(name, create, size)
    createTubes(pathTube1, pathTube2)

    launchPrimaryServer(sharedMemory.name, pathTube1, pathTube2, host, primaryServerPort)
    launchSecondaryServer(sharedMemory.name, pathTube1, pathTube2, host, secondaryServerPort)

    os.wait()

    print("Terminating children")
    activeChildren = terminateChildren()
    for child in activeChildren:
        child.join()

    print("WD> Freeing communication systems")
    freeCommunicationSystem(name, pathTube1, pathTube2)
    sys.exit(os.EX_OK)


def launchPrimaryServer(sharedMemoryName, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("WD> Fork failed\n")
        os.abort()
    elif newPid == 0:
        linkToWatchDogThread = Thread(target=linkToWatchDog, args=(host, port))
        linkToWatchDogThread.start()
        primaryServerBehaviorThread = Thread(target=primaryServerBehavior, args=(sharedMemoryName, pathTube1, pathTube2))
        primaryServerBehaviorThread.start()
        primaryServerBehaviorThread.join()
        linkToWatchDogThread.join()
        sys.exit(os.EX_OK)
    else:
        openWatchDogConnectionThread = Thread(target=openWatchDogConnection, args=(sharedMemoryName, pathTube1, pathTube2, host, port))
        openWatchDogConnectionThread.start()


def launchSecondaryServer(sharedMemoryName, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("WD> Fork failed\n")
        os.abort()
    elif newPid == 0:
        linkToWatchDogThread = Thread(target=linkToWatchDog, args=(host, port))
        linkToWatchDogThread.start()
        secondaryServerBehaviorThread = Thread(target=secondaryServerBehavior, args=(sharedMemoryName, pathTube1, pathTube2))
        secondaryServerBehaviorThread.start()
        secondaryServerBehaviorThread.join()
        linkToWatchDogThread.join()
        sys.exit(os.EX_OK)
    else:
        openWatchDogConnectionThread = Thread(target=openWatchDogConnection, args=(sharedMemoryName, pathTube1, pathTube2, host, port))
        openWatchDogConnectionThread.start()


def openWatchDogConnection(sharedMemoryName, pathTube1, pathTube2, host, port):
    watchDogSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    counter = 0

    try:
        watchDogSocket.bind((host, port))
    except socket.error:
        print('WD> Could not initialise connexion on port ', port)
        sys.exit()

    print('WD> Ready on port ', port)
    watchDogSocket.listen(2)

    connexion, address = watchDogSocket.accept()
    print('WD> Connexion with server established\n')

    while True:

        if counter < 5:
            print("WD> Are you alive ?")
            connexion.send(bytes('Are you alive ?', 'UTF-8'))
            break
        else:
            print("WD> EXIT")
            connexion.send(bytes('EXIT', 'UTF-8'))

        connexion.recv(1024).decode('UTF-8')
        time.sleep(2)
        counter += 1

    print('WD> Connexion with server closed\n')
    connexion.close()

    watchDogSocket.close()
    del watchDogSocket


def linkToWatchDog(host, port):
    attempt = 0
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while attempt < 5:
        try:
            attempt += 1
            serverSocket.connect((host, port))
            break
        except socket.error:
            if attempt >= 5:
                print("Server> Connexion to watch dog failed\n")
                sys.exit()
            time.sleep(5)
    print("Server> Connexion with watch dog established\n")

    while True:
        messageRecieved = serverSocket.recv(1024).decode('UTF-8')
        if messageRecieved.upper() == "EXIT":
            print("Server> Receiving EXIT code, stopping process\n")
            break
        print("server> Still alive !")
        serverSocket.send(bytes('Still alive !', 'UTF-8'))
        time.sleep(random.randint(2, 6))

    serverSocket.close()
    del serverSocket
