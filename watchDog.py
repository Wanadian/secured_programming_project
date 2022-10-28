#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import socket
import sys
import time


def linkPrimaryServer(host, port):
    # cpt = 0

    time.sleep(2)
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect((host, port))
    except socket.error:
        print("\nConnexion au serveur impossible à {}:{} !\n".format(host, port))
        sys.exit()
    print("Connexion établie avec le serveur de test ({}:{}).".format(host, port))

    msgServeurraw = mySocket.recv(1024)
    msgServeur = msgServeurraw.decode('UTF-8')

    # while True:
    #     if msgServeur.upper() == "FIN":
    #         break
    #     print("ServeurParent>", msgServeur)
    #
    #     if (cpt < 3):
    #         msgClient = bytes('Connexion watch ok', 'UTF-8')
    #         cpt += 1
    #         mySocket.send(msgClient)
    #         time.sleep(2)
    #     else:
    #         msgClient = bytes('FIN', 'UTF-8')
    #         mySocket.send(msgClient)
    #         break
    while True:
        print('Serveur prêt, en attente de requêtes sur {}:{}...'.format(host, port))
        mySocket.listen(5)

        connexion, adresse = mySocket.accept()
        print('Client connecté, adresse IP %s, port %s' % (adresse[0], adresse[1]))
        print('Tapez le mot FIN pour terminer.')

        connexion.send(bytes(
            'Vous etes connecte au serveur de test. Envoyez vos messages (sur une ligne) ou le mot FIN pour terminer.',
            'UTF-8'))

        while True:
            msgClientraw = connexion.recv(1024)
            msgClient = msgClientraw.decode('UTF-8')
            print('Client>', msgClient)
            if msgClient.upper() == 'FIN' or msgClient == '':
                break
            msgServeur = bytes(input('Serveur> '), 'UTF-8')
            connexion.send(msgServeur)

        connexion.send(bytes('Fin de connexion !', 'UTF-8'))
        print('Connexion interrompue.')
        connexion.close()

        ch = input('<R>ecommencer <T>erminer ? ')
        if ch.upper() == 'T':
            break

    print("Connexion interrompue. Watchdog")
    time.sleep(2)
    mySocket.close()
    del mySocket


def linkSecondaryServer(host, port):
    cpt = 0

    time.sleep(2)
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect((host, port))
    except socket.error:
        print("\nConnexion au serveur impossible à {}:{} !\n".format(host, port))
        sys.exit()
    print("Connexion établie avec le serveur de test ({}:{}).".format(host, port))

    msgServeurraw = mySocket.recv(1024)
    msgServeur = msgServeurraw.decode('UTF-8')

    # while True:
    #     if msgServeur.upper() == "FIN":
    #         break
    #     print("ServeurParent>", msgServeur)
    #
    #     if (cpt < 3):
    #         msgClient = bytes('Connexion watch ok', 'UTF-8')
    #         cpt += 1
    #         mySocket.send(msgClient)
    #         time.sleep(2)
    #     else:
    #         msgClient = bytes('FIN', 'UTF-8')
    #         mySocket.send(msgClient)
    #         break

    while True:
        msgServeurraw = mySocket.recv(1024)
        msgServeur = msgServeurraw.decode('UTF-8')
        if msgServeur.upper() == "FIN" or msgServeur == "":
            break
        print("Serveur>", msgServeur)
        msgClient = bytes(input("Client> "), 'UTF-8')
        mySocket.send(msgClient)
        if msgClient.upper() == "FIN" or msgClient == "":
            break

    print("Connexion interrompue. Watchdog")
    time.sleep(2)
    mySocket.close()
    del mySocket


def communicationWithWatchDog(host, port):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        mySocket.bind((host, port))
    except socket.error:
        print('\nImpossible d\'établir la liaison du socket à l\'adresse choisie ({}:{}) -- Parent !\n'.format(
            host, port))
        sys.exit()
    while True:
        print('Serveur prêt, en attente de requêtes sur {}:{}.. -- Parent.'.format(host, port))
        mySocket.listen(5)

        connexion, address = mySocket.accept()
        print('Client connecté, adresse IP %s, port %s' % (address[0], address[1]))

        connexion.send(bytes('Connected to server', 'UTF-8'))
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
