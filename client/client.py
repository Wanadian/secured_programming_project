import socket
import sys
import time

from server.action import delete_socket


def simulate_client():
    server_host = '127.0.0.1'
    server_port = 11111
    counter = 0

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_host, server_port))
    except socket.error:
        delete_socket(client_socket)
        sys.exit("Connexion to server failed")

    print("Connexion with server established")

    while True:
        if counter < 5:
            print("Client> ping")
            client_socket.send(bytes("ping", 'UTF-8'))
        else:
            print("Client> exit")
            client_socket.send(bytes("exit", 'UTF-8'))
            break
        message_received = client_socket.recv(1024).decode('UTF-8')
        print("Server> ", message_received)
        time.sleep(2)
        counter += 1

    delete_socket(client_socket)
    sys.exit("Simulation completed")



