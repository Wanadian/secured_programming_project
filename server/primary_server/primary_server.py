#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import socket
import sys
import time
from multiprocessing import shared_memory
from server.action import fill_shared_memory, delete_socket, create_socket


def primary_server_behavior(shared_memory_name, path_tube_1, path_tube_2):
    host = '127.0.0.1'
    client_port = 11111
    attempt = 0

    shared_memory_primary_server = shared_memory.SharedMemory(shared_memory_name)

    try:
        fifo1 = open(path_tube_1, "w")
        fifo2 = open(path_tube_2, "r")
    except BrokenPipeError as error:
        sys.exit("Could not open tubes : " + error)

    server_socket = create_socket()

    while attempt < 5:
        try:
            attempt += 1
            server_socket.bind((host, client_port))
            break
        except socket.error:
            if attempt >= 5:
                delete_socket(server_socket)
                print('Primary server> Could not initialise connection on client_port ', client_port)
                sys.exit("Server could not initialise connection")
            else:
                delete_socket(server_socket)
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(1)

    print('Primary server> Ready on port ', client_port)
    server_socket.listen(10)

    connection, address = server_socket.accept()

    while True:
        message_received = connection.recv(1024).decode('UTF-8')
        if message_received == "ping":
            print("Primary server> Ping received from a client")
            fill_shared_memory(shared_memory_primary_server, bytes(str(address), 'UTF-8'))
            try:
                fifo1.write("A client pinged\n")
                fifo1.flush()
                fifo2.readline()
            except BrokenPipeError as error:
                sys.exit("Tube not found" + error)
            try:
                connection.send(bytes("ping", 'UTF-8'))
            except BrokenPipeError as error:
                sys.exit("Connection not found" + error)
            print("Primary server> Reply sent to client")
        elif message_received == "exit":
            try:
                fifo1.write("exit\n")
                fifo1.flush()
            except BrokenPipeError as error:
                sys.exit("Tube not found" + error)
            break

    connection.close()

    delete_socket(server_socket)

    print('Primary server> Connexion with client closed')

    shared_memory_primary_server.close()

    fifo1.close()
    fifo2.close()
