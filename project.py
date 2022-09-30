#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Faire la gestion des erreurs et les codes de retours
#
# Version 27/09/2022
#
import os
from multiprocessing import shared_memory

shm_segment1 = shared_memory.SharedMemory(name='leclerc', create=True, size=10)
print('Nom du segment mémoire partagée :', shm_segment1.name)
print('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
shm_segment1.buf[:10] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

print('Création des tubes...')

pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
pathTube2 = "/tmp/tubenommesecondprincipal.fifo"

os.mkfifo(pathTube1, 0o0600)
os.mkfifo(pathTube2, 0o0600)

newPid = os.fork()
if newPid < 0:
    print("fork() impossible")
    os.abort()
elif newPid == 0:
    print('Ouverture du tube1 en écriture...')
    fifo1 = open(pathTube1, "w")
    print('Ouverture du tube2 en lecture...')
    fifo2 = open(pathTube2, "r")

    for i in range(3):
        print('Processus principal prêt pour échanger des messages...')
        print('Écriture dans le tube1...')
        fifo1.write("Message du processus principal!\n")
        fifo1.flush()
        print('Processus principal en attente de réception de messages...')
        line = fifo2.readline()
        print("Message recu : " + line)

    print('Fermeture du tube1...')
    fifo1.close()
    print('Fermeture du tube2...')
    fifo2.close()
    print('Destruction des tubes...')
    print('Destruction des tubes...')
    os.unlink(pathTube1)
    os.unlink(pathTube2)
    os.execlp("ipcs", "ipcs", "-m")
else:
    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)
    print('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf[:10]))
    print('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf[:10]))
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
    shm_segment2.close()

shm_segment1.close()
shm_segment1.unlink()
