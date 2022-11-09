#! /usr/bin/env python3
# _*_ coding: utf8 _*_
import sys
from multiprocessing import shared_memory

from server.action import fillSharedMemory


def secondaryServerBehavior(sharedMemoryName, pathTube1, pathTube2):
    sharedMemorySecondaryServer = shared_memory.SharedMemory(sharedMemoryName)
    try:
        fifo1 = open(pathTube1, "r")
        fifo2 = open(pathTube2, "w")
    except OSError as error:
        print(error, "\n")
        sys.exit("An error has occured while communicating with secondary server : ")

    while True:
        print('SS> Attente de réception de messages...\n')
        fifo1.readline()
        clientMessage = str(bytes(sharedMemorySecondaryServer.buf), 'UTF-8')
        if clientMessage == "bye":
            fifo2.write("shutdown")
            fifo2.flush()
            break
        else:
            fillSharedMemory(sharedMemorySecondaryServer, bytes("hello", 'UTF-8'))
            fifo2.write("Answer sent\n")
            fifo2.flush()


    sharedMemorySecondaryServer.close()

    try:
        fifo1.close()
        fifo2.close()
    except OSError as error:
        print(error, "\n")
        sys.exit("An error has occurred while communicating with secondary server : ")
