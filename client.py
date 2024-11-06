import socket

def client_yahtzee():
    hote = '127.0.0.1'  # Adresse IP du serveur (ici en local)
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hote, port))

    # Recevoir et afficher le message du serveur
    message = client_socket.recv(1024).decode('utf-8')
    print(message)
    
    # Envoyer le nom du joueur
    nom = input("Entrez votre nom : ")
    client_socket.sendall(nom.encode('utf-8'))

    # Communication avec le serveur
    try:
        while True:
            message_a_envoyer = input(f"{nom} > ")
            if message_a_envoyer.lower() == "quit":
                break
            client_socket.sendall(message_a_envoyer.encode('utf-8'))
            reponse = client_socket.recv(1024).decode('utf-8')
            print(f"Serveur : {reponse}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    client_yahtzee()
