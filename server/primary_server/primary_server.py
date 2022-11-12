#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import socket
import sys
import time
from multiprocessing import shared_memory
from server.action import fill_shared_memory


def primary_server_behavior(shared_memory_name, path_tube_1, path_tube_2):
    host = '127.0.0.1'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attempt = 0

    shared_memory_primary_server = shared_memory.SharedMemory(shared_memory_name)
    try:
        fifo1 = open(path_tube_1, "w")
        fifo2 = open(path_tube_2, "r")
    except OSError as error:
        print(error, "\n")
        sys.exit("An error has occured while communicating with primary server : ")

    while attempt < 5:
        try:
            attempt += 1
            server_socket.bind((host, port))
            break
        except socket.error:
            server_socket.close()
            if attempt >= 5:
                print('Primary server> Could not initialise connexion on port ', port)
                sys.exit("Server could not initialise connexion")
            time.sleep(1)

    print('Primary server> Ready on port ', port)
    server_socket.listen(10)

    connexion, address = server_socket.accept()

    while True:
        message_received = connexion.recv(1024).decode('UTF-8')
        if message_received == "ping":
            print("Primary server> Ping received from a client")
            fill_shared_memory(shared_memory_primary_server, bytes(str(address), 'UTF-8'))
            fifo1.write("A client pinged\n")
            fifo1.flush()
            fifo2.readline()
            connexion.send(bytes("ping", 'UTF-8'))
            print("Primary server> Reply sent to client")
        elif message_received == "exit":
            fifo1.write("exit\n")
            fifo1.flush()
            break

    connexion.close()
    server_socket.close()
    del server_socket

    print('Primary server> Connexion with client closed\n')

    shared_memory_primary_server.close()

    try:
        fifo1.close()
        fifo2.close()
    except OSError as error:
        print(error, "\n")
        pass
