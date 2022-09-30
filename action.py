#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os
from multiprocessing import shared_memory
from builtins import OSError
from asyncio.windows_events import NULL
from childBehavior import childBehavior
from parentBehavior import parentBehavior


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


def fillSharedMemory(shareMemory, data):
    shareMemory.buf[:shareMemory.size] = data


def closeSegments(shareMemory):
    shareMemory.close()
    shareMemory.unlink()


def createChild(shareMemory, pathTube1, pathTube2):
    newPid = os.fork()
    if newPid < 0:
        print("fork() impossible")
        os.abort()
    elif newPid == 0:
        parentBehavior(pathTube1, pathTube2)
    else:
        childBehavior(shareMemory, pathTube1, pathTube2)
