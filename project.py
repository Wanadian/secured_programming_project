import os
import shutil

print('Création des tubes...');

pathTube1 = "/tmp/tubenommeprincipalsecond.fifo"
pathTube2 = "/tmp/tubenommesecondprincipal.fifo"
try:
    os.mkfifo(pathTube1, 0o0600);
    os.mkfifo(pathTube2, 0o0600);
except shutil.Error as error:
    print(error);

newPid = os.fork();

print('Ouverture du tube1 en écriture...');
fifo1 = open(pathTube1, "w");

print('Ouverture du tube2 en lecture...');
fifo2 = open(pathTube2, "r");

#=============================================

print('Ouverture du tube1Bis en lecture...');
fifo1Bis = open(pathTube1, "r");

print('Ouverture du tube2Bis en écriture...');
fifo2Bis = open(pathTube2, "w");

#=============================================

for i in range(3):
    print('Processus principal prêt pour échanger des messages...');
    print('Écriture dans le tube1...');
    fifo1.write("Message du processus principal!\n");
    fifo1.flush();
    print('Processus principal en attente de réception de messages...');
    line = fifo2.readline();
    print("Message recu : " + line);

    print('Processus secondaire prêt pour échanger des messages...');
    print('Écriture dans le tube2...');
    fifo2Bis.write("Message du process secondaire !\n");
    fifo2Bis.flush();
    print('Processus secondaire en attente de réception de messages...');
    line = fifo1Bis.readline();
    print("Message recu : " + line);




print('Fermeture du tube1...');
fifo1.close();

print('Fermeture du tube2...');
fifo2.close();

print('Fermeture du tube1...');
fifo1Bis.close();

print('Fermeture du tube2...');
fifo2Bis.close();



print('Destruction des tubes...');
os.unlink(pathTube1);
os.unlink(pathTube2);