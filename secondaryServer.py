#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os, sys
from multiprocessing import shared_memory


def secondaryServerBehavior(sharedMemory, pathTube1, pathTube2):
    try:
        sharedMemoryC = shared_memory.SharedMemory(sharedMemory.name)
        print('Taille du segment mémoire partagée en octets via second accès :', len(sharedMemoryC.buf[:len(sharedMemory.buf)]))
        print('Contenu du segment mémoire partagée en octets via second accès :', bytes(sharedMemoryC.buf[:len(sharedMemory.buf)]))
        print('Ouverture du tube1 en lecture...')
        fifo1 = open(pathTube1, "r")
        print('Ouverture du tube2 en écriture...')
        fifo2 = open(pathTube2, "w")

        for i in range(3):
            print('Processus secondaire prêt pour échanger des messages...')
            print('Processus secondaire en attente de réception de messages...')
            line = fifo1.readline()
            print("Message recu : " + line)
            print('Écriture dans le tube2...')
            fifo2.write("Message du process secondaire !\n")
            fifo2.flush()

        print('Fermeture du tube1...')
        fifo1.close()
        print('Fermeture du tube2...')
        fifo2.close()
        os.wait()
        sharedMemoryC.close()
        sharedMemoryC.unlink()
        sys.exit(0)
    except OSError as error:
        print("Error:", error)