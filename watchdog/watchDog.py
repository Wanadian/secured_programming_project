#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 11/10/2022
#
import socket, sys


def watchDog():
    HOST = '127.0.0.1'
    PORT = 2222
    cpt = 0

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        print ("\nConnexion impossible à {}:{} !\n".format(HOST, PORT))
        sys.exit()
    print ("Connexion établie avec le serveur de test ({}:{}).".format(HOST, PORT))

    while True:
        msgServeurraw = mySocket.recv(1024)
        msgServeur = msgServeurraw.decode('UTF-8')
        if msgServeur.upper() == "FIN":
            break
        print ("ServeurParent>", msgServeur)

        if (cpt < 3):
            msgClient = bytes('Connexion watch ok', 'UTF-8')
        else:
            msgClient = bytes('FIN', 'UTF-8')
        cpt+=1
        mySocket.send(msgClient)
        if msgClient.upper() == "FIN":
            break

    print ("Connexion interrompue.")
    mySocket.close()
    del mySocket
    sys.exit(0)
