#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import socket
import sys
import time
from multiprocessing import shared_memory
from server.action import fillSharedMemory, emptySharedMemory

def primaryServerBehavior(sharedMemoryName, pathTube1, pathTube2):
    host = '127.0.0.1'
    port = 12245
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attempt = 0

    sharedMemoryPrimaryServer = shared_memory.SharedMemory(sharedMemoryName)
    try:
        fifo1 = open(pathTube1, "w")
        fifo2 = open(pathTube2, "r")
    except OSError as error:
        print(error, "\n")
        sys.exit("An error has occured while communicating with primary server : ")

    while attempt < 5:
        try:
            attempt += 1
            serverSocket.bind((host, port))
            break
        except socket.error:
            serverSocket.close()
            if attempt >= 5:
                print('Server> Could not initialise connexion on port ', port)
                sys.exit("Server could not initialise connexion")
            time.sleep(1)

    print('SP> Ready on port ', port)
    serverSocket.listen(10)

    connexion, address = serverSocket.accept()
    print('SP> Connexion with server established\n')

    while True:
        messageRecieved = connexion.recv(1024).decode('UTF-8')
        if messageRecieved == "ping":
            print("PS> Ping received from a client")
            emptySharedMemory(sharedMemoryPrimaryServer)
            fillSharedMemory(sharedMemoryPrimaryServer, bytes(str(address), 'UTF-8'))
            fifo1.write("A client pinged\n")
            fifo1.flush()
            fifo2.readline()
            connexion.send(bytes("ping", 'UTF-8'))
            print("SP> Reply sent to client")
        elif messageRecieved == "exit":
            fifo1.write("exit\n")
            fifo1.flush()
            break

    connexion.close()
    serverSocket.close()
    del serverSocket

    print('SP> Connexion with client closed\n')

    sharedMemoryPrimaryServer.close()

    try:
        fifo1.close()
        fifo2.close()
    except OSError as error:
        print(error, "\n")
        pass
