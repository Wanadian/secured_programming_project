import os

print('Création des tubes...')

pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
pathTube2 = "/tmp/tubenommesecondprincipal.fifo"

os.mkfifo(pathTube1, 0o0600)
os.mkfifo(pathTube2, 0o0600)

newPid = os.fork()
if newPid < 0:
    print("fork() impossible")
    os.abort()
elif newPid == 0:
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

else:
    print('Ouverture du tube1 en lecture...')
    fifo1 = open(pathTube1, "r")
    print('Ouverture du tube2 en écriture...')
    fifo2 = open(pathTube2, "w")

    for i in range(3):
        print('Processus secondaire prêt pour échanger des messages...')
        print('Processus secondaire en attente de réception de messages...')
        line = fifo1.readline()
        print("Message recu : " + line)
        print('Écriture dans le tube2...')
        fifo2.write("Message du process secondaire !\n")
        fifo2.flush()

    print('Fermeture du tube1...')
    fifo1.close()
    print('Fermeture du tube2...')
    fifo2.close()
