#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os
from multiprocessing import shared_memory

def childBehavior(shareMemory, pathTube1, pathTube2):
    shareMemoryC = shared_memory.SharedMemory(shareMemory.name)
    print('Taille du segment mémoire partagée en octets via second accès :', len(shareMemoryC.buf[:shareMemoryC.size]))
    print('Contenu du segment mémoire partagée en octets via second accès :', bytes(shareMemoryC.buf[:shareMemoryC.size]))
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
    shareMemoryC.close()