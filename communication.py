#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os
from multiprocessing import shared_memory
from builtins import OSError
from asyncio.windows_events import NULL


def createTubes(pathTube1, pathTube2):
    print('Création des tubes...')

    try:
        os.mkfifo(pathTube1, 0o0600)
        os.mkfifo(pathTube2, 0o0600)
    except OSError as error:
        print("Error: ", error)


def createSharedMemory(name, create, size):
    try:
        return shared_memory.SharedMemory(name, create, size)
    except (ValueError, FileExistsError, OSError) as error:
        print("Error: ", error)
    return NULL


def fillSharedMemory(segment, data):
    segment.buf[:segment.size] = data


def closeSegments(segment):
    segment.close()
    segment.unlink()


def createChild(fifoP1, fifoP2, fifoF1, fifoF2, segmentP, segmentF, pathTube1, pathTube2):
    newPid = os.fork()
    if newPid < 0:
        print("fork() impossible")
        os.abort()
    elif newPid == 0:
        print("pere")
    else:
        print("fils")


def main():
    pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
    pathTube2 = "/tmp/tubenommesecondprincipal.fifo"

    createTubes(pathTube1, pathTube2)