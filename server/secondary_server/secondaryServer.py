#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import sys
from multiprocessing import shared_memory
from datetime import datetime


def secondaryServerBehavior(sharedMemoryName, pathTube1, pathTube2):
    sharedMemorySecondaryServer = shared_memory.SharedMemory(sharedMemoryName)
    try:
        fifo1 = open(pathTube1, "r")
        fifo2 = open(pathTube2, "w")
    except OSError as error:
        print(error, "\n")
        sys.exit("An error has occured while communicating with secondary server : ")

    logFile = open("./log.txt", 'w')

    while True:
        primaryServerMessage = fifo1.readline()
        if primaryServerMessage == "exit\n":
            break
        else:
            clientAddress = bytes(sharedMemorySecondaryServer.buf).decode('UTF-8')
            logFile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": ping from user " + clientAddress + "\n")
            fifo2.write("ping registered\n")
            fifo2.flush()

    logFile.close()

    sharedMemorySecondaryServer.close()

    try:
        fifo1.close()
        fifo2.close()
    except OSError as error:
        print(error, "\n")
        sys.exit("An error has occurred while communicating with secondary server : ")
