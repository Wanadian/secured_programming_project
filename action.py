# CARLIER Amandine et DENORME William
#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
from multiprocessing import shared_memory, active_children
from builtins import OSError


def freeCommunicationSystem(sharedMemoryName, pathTube1, pathTube2):
    try:
        os.unlink(pathTube1)
    except OSError as error:
        print("Warning:", error)
    try:
        os.unlink(pathTube2)
    except OSError as error:
        print("Warning:", error)
    try:
        sharedMemoryToDelete = shared_memory.SharedMemory(sharedMemoryName)
        sharedMemoryToDelete.unlink()
    except OSError as error:
        print("Warning:", error)



def createTubes(pathTube1, pathTube2):
    try:
        os.mkfifo(pathTube1, 0o0600)
        os.mkfifo(pathTube2, 0o0600)
    except OSError as error:
        print("An error occured in fonction createTubes in file action:", error)


def createdSharedMemory(name, create, size):
    try:
        return shared_memory.SharedMemory(name, create, size)
    except (ValueError, FileExistsError, OSError) as error:
        print("An error occured in fonction createdSharedMemory in file action:", error)


def fillSharedMemory(sharedMemory, data):
    sharedMemory.buf[:len(data)] = data


def raiseTimeoutError(signum, frame):
    raise TimeoutError


def terminateChildren():
    activeChildren = active_children()
    for child in activeChildren:
        child.terminate()
    print("All child processe(s) terminated")
    return activeChildren
