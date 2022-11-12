#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import socket
import sys
import time
from threading import Thread
from server.action import created_shared_memory, create_tubes, free_communication_system, terminate_children, \
    delete_socket
from server.primary_server.primary_server import primary_server_behavior
from server.secondary_server.secondary_server import secondary_server_behavior


def launch_watch_dog():
    host = '127.0.0.1'
    primary_server_port = 22222
    secondary_server_port = 33333

    path_tube1 = "/tmp/tubenommeprincipalsecond.fifo"
    path_tube2 = "/tmp/tubenommesecondprincipal.fifo"

    name = "leclerc"
    create = True

    free_communication_system(name, path_tube1, path_tube2)

    shared_memory = created_shared_memory(name, create)
    create_tubes(path_tube1, path_tube2)

    open_watch_dog_connection_thread1 = Thread(target=open_watch_dog_connection, name="watch_Dog_to_primary_server", args=(host, primary_server_port))
    open_watch_dog_connection_thread2 = Thread(target=open_watch_dog_connection, name="watch_dog_to_secondary_server", args=(host, secondary_server_port))
    open_watch_dog_connection_thread1.start()
    open_watch_dog_connection_thread2.start()

    launch_primary_server(shared_memory.name, path_tube1, path_tube2, host, primary_server_port)
    launch_secondary_server(shared_memory.name, path_tube1, path_tube2, host, secondary_server_port)

    open_watch_dog_connection_thread1.join()
    open_watch_dog_connection_thread2.join()

    os.wait()

    active_children = terminate_children()
    for child in active_children:
        child.join()
    free_communication_system(name, path_tube1, path_tube2)
    sys.exit(os.EX_OK)


def launch_primary_server(shared_memory_name, path_tube_1, path_tube_2, host, port):
    new_pid = os.fork()

    if new_pid < 0:
        print("WD> Fork failed\n")
        os.abort()
    elif new_pid == 0:
        link_to_watch_dog_thread = Thread(target=link_to_watch_dog, name="primary_server_to_watch_dog", args=(host, port))
        primary_server_behavior_thread = Thread(target=primary_server_behavior, name="primary_server_behavior", args=(shared_memory_name, path_tube_1, path_tube_2))
        link_to_watch_dog_thread.start()
        primary_server_behavior_thread.start()
        primary_server_behavior_thread.join()
        link_to_watch_dog_thread.join()
        sys.exit(os.EX_OK)


def launch_secondary_server(shared_memory_name, path_tube_1, path_tube_2, host, port):
    new_pid = os.fork()

    if new_pid < 0:
        print("WD> Fork failed\n")
        os.abort()
    elif new_pid == 0:
        link_to_watch_dog_thread = Thread(target=link_to_watch_dog, name="secondary_server_to_watch_dog", args=(host, port))
        secondary_server_behavior_thread = Thread(target=secondary_server_behavior, name="secondary_server_behavior", args=(shared_memory_name, path_tube_1, path_tube_2))
        link_to_watch_dog_thread.start()
        secondary_server_behavior_thread.start()
        secondary_server_behavior_thread.join()
        link_to_watch_dog_thread.join()
        sys.exit(os.EX_OK)


def open_watch_dog_connection(host, port):
    watch_dog_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    counter = 0
    attempt = 0
    while attempt < 5:
        try:
            attempt += 1
            watch_dog_socket.bind((host, port))
            break
        except socket.error:
            if attempt >= 5:
                delete_socket(watch_dog_socket)
                print('Watch dog> Could not initialise connexion on port ', port)
                return
            else:
                delete_socket(watch_dog_socket)
                watch_dog_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(1)

    print('Watch dog> Ready on port ', port)
    watch_dog_socket.listen(1)

    connexion, address = watch_dog_socket.accept()

    while True:
        if counter < 5:
            print("Watch dog> Are you alive ?")
            connexion.send(bytes('Are you alive ?', 'UTF-8'))
        else:
            print("Watch dog> EXIT")
            connexion.send(bytes('EXIT', 'UTF-8'))
            break
        connexion.recv(1024).decode('UTF-8')
        time.sleep(2)
        counter += 1

    print('Watch dog> Connexion with server closed')
    connexion.close()
    delete_socket(watch_dog_socket)


def link_to_watch_dog(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect((host, port))
    except socket.error:
        delete_socket(server_socket)
        sys.exit("Connexion to watch dog failed")
    print("Server> Connexion to watch dog established")

    while True:
        message_received = server_socket.recv(1024).decode('UTF-8')
        if message_received.upper() == "EXIT":
            print("Server> Receiving EXIT code, stopping process")
            break
        print("server> Still alive !")
        server_socket.send(bytes('Still alive !', 'UTF-8'))

    delete_socket(server_socket)
