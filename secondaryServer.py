#! /usr/bin/env python3
# _*_ coding: utf8 _*_
import os
import sys
from multiprocessing import shared_memory


def secondaryServerBehavior(sharedMemory, pathTube1, pathTube2):
    sharedMemorySecondaryServer(sharedMemory, pathTube1, pathTube2)
    sys.exit(0)


def sharedMemorySecondaryServer(sharedMemory, pathTube1, pathTube2):
    try:
        sharedMemoryC = shared_memory.SharedMemory(sharedMemory.name)
        fifo1 = open(pathTube1, "r")
        fifo2 = open(pathTube2, "w")
        print('SS> Prêt\n')

        for i in range(3):
            print('SS> Attente de réception de messages...\n')
            line = fifo1.readline()
            print("SS> Message recu : " + line + "\n")
            print('SS> Écriture dans le tube2...\n')
            fifo2.write("Message du process secondaire !")
            fifo2.flush()

        fifo1.close()
        fifo2.close()
        os.wait()
        sharedMemoryC.close()
        sharedMemoryC.unlink()
    except OSError as error:
        print("An error occured:", error)
