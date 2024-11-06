import socket
import threading
import random


# Dictionnaire pour stocker les noms des clients et leur adresse
clients_connectes = {}


def dice(nb_lancer_max):
    for i in range(1,nb_lancer_max+1):
        random_numbers = [random.randint(1, 6) for _ in range(6)]
      #  print(random_numbers)
        return random_numbers





def gerer_client(connexion, adresse):
    print(f"Nouvelle connexion : {adresse}")
    
    # Recevoir le nom du client
    connexion.sendall("Veuillez entrer votre nom : ".encode('utf-8'))
    nom_client = connexion.recv(1024).decode('utf-8')
    
    # Ajouter le client à la liste des clients connectés
    clients_connectes[nom_client] = adresse
    print(f"{nom_client} (adresse : {adresse}) est maintenant connecté.")
    print(f"Nombre de clients connectés : {len(clients_connectes)}")
    
    try:
        while True:
            data = connexion.recv(1024)
            if not data:
                break
            print(f"Reçu de {nom_client} : {data.decode()}")
            connexion.sendall("Message reçu".encode('utf-8'))
    finally:
        connexion.close()
        del clients_connectes[nom_client]  # Retirer le client du dictionnaire
        print(f"{nom_client} déconnecté.")
        print(f"Nombre de clients connectés : {len(clients_connectes)}")

def serveur_yahtzee():
    hote = '0.0.0.0'
    port = 12345
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.bind((hote, port))
    serveur_socket.listen(5)

    print(f"Serveur Yahtzee démarré sur {hote}:{port}")

    while True:
        connexion, adresse = serveur_socket.accept()
        thread = threading.Thread(target=gerer_client, args=(connexion, adresse))
        thread.start()

if __name__ == "__main__":
    serveur_yahtzee()
