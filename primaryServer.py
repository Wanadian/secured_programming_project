#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os

from action import fillSharedMemory, createTubes, closeSegments, createdSharedMemory
from secondaryServer import secondaryServerBehavior
from watchDog import openWatchDogConnection


def primaryServerBehavior():
    host = '127.0.0.1'
    port = 2222

    name = "leclerc"
    create = True
    size = 10
    data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
    pathTube2 = "/tmp/tubenommesecondprincipal.fifo"

    sharedMemory = createdSharedMemory(name, create, size)
    fillSharedMemory(sharedMemory, data)
    createTubes(pathTube1, pathTube2)
    launchSecondaryServer(sharedMemory, pathTube1, pathTube2, host, port)
    closeSegments(sharedMemory)


def communicationSecondaryServer(pathTube1, pathTube2):
    try:
        print('Server> Ouverture du tube1 en écriture...')
        fifo1 = open(pathTube1, "w")
        print('Server> Ouverture du tube2 en lecture...')
        fifo2 = open(pathTube2, "r")
        print('Server> Prêt')

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


def launchSecondaryServer(shareMemory, pathTube1, pathTube2, host, port):
    newPid = os.fork()

    if newPid < 0:
        print("Server> fork impossible")
        os.abort()
    elif newPid == 0:
        # openWatchDogConnection(host, port)
        communicationSecondaryServer(pathTube1, pathTube2)
    else:
        secondaryServerBehavior(shareMemory, pathTube1, pathTube2, host, port)
