#! /usr/bin/env python3
# _*_ coding: utf8 _*_
import os
import sys
import time
from multiprocessing import shared_memory


def secondaryServerBehavior(sharedMemoryName, pathTube1, pathTube2):
    sharedMemorySecondaryServer = shared_memory.SharedMemory(sharedMemoryName)
    communicationWithPrimaryServer(pathTube1, pathTube2)
    sharedMemorySecondaryServer.close()
    sys.exit(0)


def communicationWithPrimaryServer(pathTube1, pathTube2):
    try:
        fifo1 = open(pathTube1, "r")
        fifo2 = open(pathTube2, "w")
        print('SS> Prêt\n')

        for i in range(3):
            print('SS> Attente de réception de messages...\n')
            line = fifo1.readline()
            print("SS> Message recu : " + line + "\n")
            print('SS> Écriture dans le tube2...\n')
            fifo2.write("Message du process secondaire !\n")
            fifo2.flush()

        fifo1.close()
        fifo2.close()
    except OSError as error:
        print("An error occured in fonction communicationWithPrimaryServer in file action:", error)
