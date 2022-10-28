#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
from multiprocessing import shared_memory

from action import fillSharedMemory, createTubes, closeSegments, createdSharedMemory


def primaryServerBehavior(sharedMemory, pathTube1, pathTube2):
    data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    sharedMemoryPrimaryServer = shared_memory.SharedMemory(sharedMemory.name)
    fillSharedMemory(sharedMemoryPrimaryServer, data)
    createTubes(pathTube1, pathTube2)
    communicationSecondaryServer(pathTube1, pathTube2)
    closeSegments(sharedMemoryPrimaryServer)


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

