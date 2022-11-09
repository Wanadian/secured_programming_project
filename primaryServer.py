#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import time
from multiprocessing import shared_memory

from action import fillSharedMemory


def primaryServerBehavior(sharedMemoryName, pathTube1, pathTube2):
    data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])
    sharedMemoryPrimaryServer = shared_memory.SharedMemory(sharedMemoryName)
    fillSharedMemory(sharedMemoryPrimaryServer, data)
    communicationWithSecondaryServer(pathTube1, pathTube2)


def communicationWithSecondaryServer(pathTube1, pathTube2):
    try:
        fifo1 = open(pathTube1, "w")
        fifo2 = open(pathTube2, "r")
        print('SP> Prêt\n')

        for i in range(3):
            print('SP> Écriture dans le tube1...\n')
            fifo1.write("Message du SP\n")
            fifo1.flush()
            print('SP> Attente de réception de messages...\n')
            line = fifo2.readline()
            print("SP> Message recu : " + line + "\n")

        fifo1.close()
        fifo2.close()
    except OSError as error:
        print("An error occured in fonction communicationWithSecondaryServer in file action:", error)
