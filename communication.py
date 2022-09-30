#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os
from multiprocessing import shared_memory
from builtins import OSError
from asyncio.windows_events import NULL
from OSPS2022.Projet.git.secured_programming_project.childBehavior import childBehavior
from OSPS2022.Projet.git.secured_programming_project.parentBehavior import parentBehavior


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


def projet():
    name = "leclerc"
    create = True
    size = 10

    data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

    pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
    pathTube2 = "/tmp/tubenommesecondprincipal.fifo"
    
    shareMemory = createSharedMemory(name, create, size)
    fillSharedMemory(shareMemory, data)
    createTubes(pathTube1, pathTube2)
    createChild(shareMemory, pathTube1, pathTube2)
    closeSegments(shareMemory)


projet()