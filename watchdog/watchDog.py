#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Version 11/10/2022
#
import os
import socket, sys
import time
from server.parentBehavior import communicationWatchDog


def watchDog():
    HOST = '127.0.0.1'
    PORT = 1111
    cpt = 0

    newPid = os.fork()

    if newPid < 0:
        print("fork() impossible")
        os.abort()
    elif newPid == 0:
        communicationWatchDog()
    else:
        time.sleep(2)
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            mySocket.connect((HOST, PORT))
        except socket.error:
            print ("\nConnexion au serveur impossible à {}:{} !\n".format(HOST, PORT))
            sys.exit()
        print ("Connexion établie avec le serveur de test ({}:{}).".format(HOST, PORT))
        
        msgServeurraw = mySocket.recv(1024)
        msgServeur = msgServeurraw.decode('UTF-8')

        while True:
            if msgServeur.upper() == "FIN":
                break
            print ("ServeurParent>", msgServeur)

            if (cpt < 3):
                msgClient = bytes('Connexion watch ok', 'UTF-8')
                cpt+=1
                mySocket.send(msgClient)
                time.sleep(2)
            else:
                msgClient = bytes('FIN', 'UTF-8')
                mySocket.send(msgClient)
                break

        print ("Connexion interrompue. Watchdog")
        mySocket.close()
        del mySocket
        sys.exit(0)
