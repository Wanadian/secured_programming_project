#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Faire la gestion des erreurs et les codes de retours
#
# Version 27/09/2022
#
import os
from action import createSharedMemory
from action import fillSharedMemory
from action import createTubes
from action import createChild
from action import closeSegments

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