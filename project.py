#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Faire la gestion des erreurs et les codes de retours
#
# Version 27/09/2022
#

from server.action import createSharedMemory, fillSharedMemory, createTubes, createChild, closeSegments, launchWatchDog

name = "leclerc"
create = True
size = 10

data = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
pathTube2 = "/tmp/tubrm enommesecondprincipal.fifo"

shareMemory = createSharedMemory(name, create, size)
print(shareMemory)
fillSharedMemory(shareMemory, data)
createTubes(pathTube1, pathTube2)
createChild(shareMemory, pathTube1, pathTube2)
closeSegments(shareMemory)
launchWatchDog()
