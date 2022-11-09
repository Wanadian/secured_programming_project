#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import sys
from multiprocessing import shared_memory, active_children
from builtins import OSError


def createTubes(pathTube1, pathTube2):
    attempt = 0
    while attempt < 5:
        try:
            attempt += 1
            os.mkfifo(pathTube1, 0o0600)
            os.mkfifo(pathTube2, 0o0600)
            break
        except OSError:
            if attempt >= 5:
                sys.exit("Could not create tubes")

def createdSharedMemory(name, create, size):
    attempt = 0
    while attempt < 5:
        try:
            attempt += 1
            return shared_memory.SharedMemory(name, create, size)
        except (ValueError, FileExistsError, OSError):
            if attempt >= 5:
                sys.exit("Could not create shared memory")


def fillSharedMemory(sharedMemory, data):
    sharedMemory.buf[:len(data)] = data


def freeCommunicationSystem(sharedMemoryName, pathTube1, pathTube2):
    try:
        os.unlink(pathTube1)
    except OSError as error:
        print("Warning : ", error)
    try:
        os.unlink(pathTube2)
    except OSError as error:
        print("Warning : ", error)
    try:
        sharedMemoryToDelete = shared_memory.SharedMemory(sharedMemoryName)
        sharedMemoryToDelete.unlink()
    except OSError as error:
        print("Warning : ", error)


def terminateChildren():
    activeChildren = active_children()
    for child in activeChildren:
        child.terminate()
    return activeChildren


# def raiseTimeoutError(signum, frame):
#     raise TimeoutError
