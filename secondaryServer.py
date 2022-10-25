#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 30/09/2022
#
import os, sys, socket, time
from multiprocessing import shared_memory


def secondaryServerBehavior(sharedMemory, pathTube1, pathTube2, host, secondaryPort):
    sharedMemorySecondaryServer(sharedMemory, pathTube1, pathTube2)
    communicationWatchDog(host, secondaryPort)
    sys.exit(0)
    


def sharedMemorySecondaryServer(sharedMemory, pathTube1, pathTube2):
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
    except OSError as error:
        print("Error:", error)


def communicationWatchDog(hostWatchDog, portWatchDog):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        mySocket.bind((hostWatchDog, portWatchDog))
    except socket.error:
        print('\nImpossible d\'établir la liaison du socket à l\'adresse choisie ({}:{}) -- Parent !\n'.format(hostWatchDog, portWatchDog))
        sys.exit()
    while True:
        print('Serveur prêt, en attente de requêtes sur {}:{}.. -- Parent.'.format(hostWatchDog, portWatchDog))
        mySocket.listen(5)

        connexion, address = mySocket.accept()
        print('Client connecté, adresse IP %s, port %s' % (address[0], address[1]))

        connexion.send(bytes('Connected to server','UTF-8'))
        while True:
            msgClientraw = connexion.recv(1024)
            msgClient = msgClientraw.decode('UTF-8')
            print('watch dog>', msgClient)
            if msgClient.upper() == "FIN":
                break
            msgServeur = bytes('Server> Connexion ok', 'UTF-8')
            connexion.send(msgServeur)
            time.sleep(2)

        connexion.send(bytes('Fin de connexion !', 'UTF-8'))
        print('Connexion interrompue.')
        connexion.close()
        break

    mySocket.close()
    del mySocket
