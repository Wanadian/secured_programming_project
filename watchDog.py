#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import signal
import socket
import sys
import time

from action import createdSharedMemory, createTubes, freeCommunicationSystem, raiseTimeoutError
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

    print("WD> Freeing communication systems")
    freeCommunicationSystem(name, pathTube1, pathTube2)
    sys.exit(0)


def launchPrimaryServer(sharedMemoryName, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("WD> Fork failed\n")
        os.abort()
    elif newPid == 0:
        linkToWatchDog(host, port)
        primaryServerBehavior(sharedMemoryName, pathTube1, pathTube2)
        sys.exit(0)
    else:
        try:
            openWatchDogConnection(host, port)
        except ConnectionError:
            print("Connexion with primary server aborted")
            exit(-1)


def launchSecondaryServer(sharedMemoryName, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("WD> Fork failed\n")
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
        print('WD> Could not initialise connexion\n')
        sys.exit()

    print('WD> Ready\n')
    watchDogSocket.listen(2)

    connexion, address = watchDogSocket.accept()
    print('WD> Connexion with server established\n')

    while True:
        connexion.send(bytes('Are you alive ?', 'UTF-8'))

        signal.signal(signal.SIGALRM, raiseTimeoutError)
        signal.alarm(5)
        try:
            messageRecieved = connexion.recv(1024).decode('UTF-8')
            print('Server> ' + messageRecieved + "\n")
        except TimeoutError:
            print("WD> Action timeout")
            connexion.send(bytes('EXIT', 'UTF-8'))
            raise ConnectionError
            break
        finally:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)

        time.sleep(2)

    print('WD> Connexion with server closed\n')
    connexion.close()

    watchDogSocket.close()
    del watchDogSocket


def linkToWatchDog(host, port):
    attempt = 0
    cpt = 0
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
        print("WD> " + messageRecieved + "\n")
        if cpt < 5:
            serverSocket.send(bytes('Still alive !', 'UTF-8'))
        else:
            print("server> sleeping : no message sent")
            time.sleep(10)
        cpt += 1

    serverSocket.close()
    del serverSocket
