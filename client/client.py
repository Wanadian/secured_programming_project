import socket
import sys
import time


def simulateClient():
    host = '127.0.0.1'
    port = 1224
    attempt = 0
    counter = 0
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while attempt < 5:
        try:
            attempt += 1
            clientSocket.connect((host, port))
            break
        except socket.error:
            if attempt >= 5:
                clientSocket.close()
                sys.exit("Connexion to server failed")
            time.sleep(5)
    print("Client> Connexion with server established\n")

    while True:
        if counter < 5:
            print("Client> Hello")
            clientSocket.send(bytes("hello", 'UTF-8'))
        else:
            print("Client> Bye")
            clientSocket.send(bytes("bye", 'UTF-8'))
            break
        messageRecieved = clientSocket.recv(1024).decode('UTF-8')
        print("Server> ", messageRecieved)
        time.sleep(2)
        counter += 1

    clientSocket.close()
    del clientSocket
    sys.exit("Simulation completed")
