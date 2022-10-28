#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
from multiprocessing import shared_memory
from builtins import OSError


def createTubes(pathTube1, pathTube2):
    try:
        os.mkfifo(pathTube1, 0o0600)
        os.mkfifo(pathTube2, 0o0600)
    except OSError as error:
        print("An error occured:", error)


def createdSharedMemory(name, create, size):
    try:
        return shared_memory.SharedMemory(name, create, size)
    except (ValueError, FileExistsError, OSError) as error:
        print("An error occured:", error)


def fillSharedMemory(sharedMemory, data):
    sharedMemory.buf[:len(data)] = data

