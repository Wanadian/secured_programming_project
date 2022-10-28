#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
from multiprocessing import shared_memory

from action import fillSharedMemory, createTubes


def primaryServerBehavior(sharedMemory, pathTube1, pathTube2):
    data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    sharedMemoryPrimaryServer = shared_memory.SharedMemory(sharedMemory.name)
    fillSharedMemory(sharedMemoryPrimaryServer, data)
    createTubes(pathTube1, pathTube2)
    communicationWithSecondaryServer(pathTube1, pathTube2)
    sharedMemory.close()


def communicationWithSecondaryServer(pathTube1, pathTube2):
    try:
        fifo1 = open(pathTube1, "w")
        fifo2 = open(pathTube2, "r")
        print('SP> Prêt\n')

        for i in range(3):
            print('SP> Écriture dans le tube1...\n')
            fifo1.write("Message du SP !")
            fifo1.flush()
            print('SP> Attente de réception de messages...\n')
            line = fifo2.readline()
            print("SP> Message recu : " + line + "\n")

        fifo1.close()
        fifo2.close()
        os.unlink(pathTube1)
        os.unlink(pathTube2)
        os.execlp("ipcs", "ipcs", "-m")
    except OSError as error:
        print("An error occured:", error)

