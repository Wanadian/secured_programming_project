import socket
import sys
import time


def simulate_client():
    host = '127.0.0.1'
    port = 12345
    attempt = 0
    counter = 0
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while attempt < 5:
        try:
            attempt += 1
            client_socket.connect((host, port))
            break
        except socket.error:
            if attempt >= 5:
                client_socket.close()
                sys.exit("Connexion to server failed")
            time.sleep(2)
    print("Connexion with server established\n")

    while True:
        if counter < 3:
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

    client_socket.close()
    del client_socket
    sys.exit("Simulation completed")
