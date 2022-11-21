#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import os
import socket
import sys
from multiprocessing import shared_memory, active_children
from builtins import OSError

sharedMemorySize = 20


def create_tubes(path_tube_1, path_tube_2):
    try:
        os.mkfifo(path_tube_1, 0o0600)
        os.mkfifo(path_tube_2, 0o0600)
    except OSError as error:
        print(error)
        sys.exit("Could not create tubes : ")


def create_shared_memory(name, create):
    try:
        return shared_memory.SharedMemory(name, create, sharedMemorySize)
    except (ValueError, FileExistsError, OSError) as error:
        print(error)
        sys.exit("Could not create shared memory : ")


def create_socket():
    created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    created_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return created_socket


def fill_shared_memory(shared_memory, data):
    shared_memory.buf[:sharedMemorySize] = data


def free_communication_system(shared_memory_name, path_tube_1, path_tube_2):
    try:
        if(os.path.exists(path_tube_1)):
            os.unlink(path_tube_1)
    except OSError as error:
        print("Warning : ", error)
    try:
        if(os.path.exists(path_tube_2)):
            os.unlink(path_tube_2)
    except OSError as error:
        print("Warning : ", error)
    try:
        shared_memory_to_delete = shared_memory.SharedMemory(shared_memory_name)
        shared_memory_to_delete.unlink()
    except OSError as error:
        print("Warning : ", error)


def delete_socket(socket_to_delete):
    socket_to_delete.close()
    del socket_to_delete


def terminate_children():
    active_children_list = active_children()
    for child in active_children_list:
        child.terminate()
    return active_children_list
