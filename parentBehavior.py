def parentBehavior():
    print('Ouverture du tube1 en écriture...')
    fifo1 = open(pathTube1, "w")
    print('Ouverture du tube2 en lecture...')
    fifo2 = open(pathTube2, "r")

    for i in range(3):
        print('Processus principal prêt pour échanger des messages...')
        print('Écriture dans le tube1...')
        fifo1.write("Message du processus principal!\n")
        fifo1.flush()
        print('Processus principal en attente de réception de messages...')
        line = fifo2.readline()
        print("Message recu : " + line)

    print('Fermeture du tube1...')
    fifo1.close()
    print('Fermeture du tube2...')
    fifo2.close()
    print('Destruction des tubes...')
    print('Destruction des tubes...')
    os.unlink(pathTube1)
    os.unlink(pathTube2)
    os.execlp("ipcs", "ipcs", "-m")