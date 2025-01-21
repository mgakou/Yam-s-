import socket

def client_yahtzee():
    hote = '127.0.0.1'  # Adresse IP du serveur
    port = 12345        # Port du serveur

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hote, port))

    try:
        while True:
            # Recevoir un message du serveur
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                print("Connexion fermée par le serveur.")
                break

            # Afficher le message reçu
            print(data)

            # Répondre si nécessaire
            if "Choisissez un numéro" in data or "entrez 'stop'" in data:
                user_input = input("Votre choix : ")
                client_socket.sendall(user_input.encode('utf-8'))

    except KeyboardInterrupt:
        print("\nClient interrompu par l'utilisateur.")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        client_socket.close()
        print("Connexion au serveur fermée.")


if __name__ == "__main__":
    client_yahtzee()