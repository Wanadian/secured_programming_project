#! /usr/bin/env python3
# _*_ coding: utf8 _*_

import sys, os
from multiprocessing import shared_memory
from datetime import datetime


def secondary_server_behavior(shared_memory_name, path_tube_1, path_tube_2):
    if(os.path.exists("/run/shm/leclerc")):
        shared_memory_secondary_server = shared_memory.SharedMemory(shared_memory_name)

    if(os.path.exists("/tmp/tubenommeprincipalsecond.fifo") & os.path.exists("/tmp/tubenommesecondprincipal.fifo")):
        try:
            fifo1 = open(path_tube_1, "r")
            fifo2 = open(path_tube_2, "w")
        except OSError as error:
            sys.exit("Could not open tubes : ", error)

        log_file = open("./log.txt", 'a')

        while True:
            try:
                primary_server_message = fifo1.readline()
            except BrokenPipeError as error:
                sys.exit("Tube not found" + error)

            if primary_server_message == "exit\n":
                break
            elif primary_server_message == "A client pinged\n":
                try:
                    client_address = bytes(shared_memory_secondary_server.buf).decode('UTF-8')
                except BrokenPipeError as error:
                    sys.exit("Shared memory not found", error)

                log_file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": ping from user " + client_address + "\n")
                try:
                    fifo2.write("ping registered\n")
                    fifo2.flush()
                except BrokenPipeError as error:
                    sys.exit("Tube not found" + error)

        log_file.close()

        shared_memory_secondary_server.close()

        fifo1.close()
        fifo2.close()
