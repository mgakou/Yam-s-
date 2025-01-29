import socket
import threading
import random

# Configuration globale
clients_connectes = []  # Liste des connexions clients
NB_TOUR_DE_JEU = 1
lock = threading.Lock()
game_started = threading.Event()


# Fonction pour lancer les dés
def dice():
    print("Appel de la fonction dice")
    return [random.randint(1, 6) for _ in range(5)]


# Fonction pour envoyer des données au client
def send_to_player(connexion, message):
    print("Appel de la fonction sendtpplayer")
    try:
        connexion.sendall((message + "\n").encode('utf-8'))
    except Exception as e:
        print(f"Erreur lors de l'envoi des données au joueur : {e}")


# Fonction pour recevoir des données du client
def receive_from_player(connexion):
    print("Appel de la fonction receivefromplayer")
    try:
        data = connexion.recv(1024).decode('utf-8').strip()
        if not data:
            raise ValueError("Connexion fermée par le client.")
        return data
    except Exception as e:
        print(f"Erreur lors de la réception des données du joueur : {e}")
        return None

def display_score_table(scores):
    # Générer un tableau formaté
    score_table = "\n--- Tableau des Scores ---\n"
    score_table += f"{'Joueur':<20}{'Score Total':<10}\n"
    score_table += "-" * 30 + "\n"

    for connexion, score in scores.items():
        player_name = connexion.getpeername()  # Identifiant du joueur basé sur l'adresse IP
        score_table += f"{str(player_name):<20}{score:<10}\n"

    score_table += "-" * 30 + "\n"

    # Envoyer le tableau à tous les joueurs
    for connexion in clients_connectes:
        send_to_player(connexion, score_table)

    print(score_table)  # Afficher dans la console du serveur pour débogage
def game_loop():
    scores = {connexion: 0 for connexion in clients_connectes}

    # Prévenir tous les joueurs du début de la partie
    for connexion in clients_connectes:
        send_to_player(connexion, "La partie commence !")

    # Gérer les tours
    for tour in range(NB_TOUR_DE_JEU):
        for connexion in clients_connectes:
            current_score = 0
            send_to_player(connexion, f"Début du tour {tour + 1}. Votre score total est : {scores[connexion]}")

            for lancer in range(3):  # Jusqu'à 3 lancers
                dice_result = dice()
                send_to_player(connexion, f"Lancer {lancer + 1} : {dice_result}")
                send_to_player(connexion, "Choisissez un numéro à conserver ou entrez 'stop' pour terminer ce tour :")
                choice = receive_from_player(connexion)

                if choice == "stop":
                    send_to_player(connexion, f"Fin de votre tour. Score total du tour : {current_score}")
                    break
                else:
                    try:
                        chosen_number = int(choice)
                        score_for_this_roll = sum(d for d in dice_result if d == chosen_number)
                        current_score += score_for_this_roll
                        send_to_player(connexion, f"Vous avez conservé les {chosen_number}. Score du lancer : {score_for_this_roll}")
                        send_to_player(connexion, f"Score accumulé ce tour : {current_score}")
                    except ValueError:
                        send_to_player(connexion, "Entrée invalide. Réessayez.")

            scores[connexion] += current_score
            send_to_player(connexion, f"Tour terminé. Votre score total est maintenant : {scores[connexion]}")

    # Afficher et envoyer le tableau des scores à tous les joueurs
    display_score_table(scores)


# Fin de partie
def end_game(scores):
    print("Appel de la fonction end_game")
    print("Partie terminée !")
    for connexion, score in scores.items():
        print(f"Joueur {connexion.getpeername()} : {score} points")
    winner = max(scores, key=scores.get)
    print(f"Le gagnant est le joueur {winner.getpeername()} avec {scores[winner]} points !")
    for connexion in clients_connectes:
        send_to_player(connexion, "Partie terminée ! Merci d'avoir joué.")


condition = threading.Condition()  # Pour synchroniser les threads des clients

def gerer_client(connexion, adresse):
    try:
        print(f"Nouvelle connexion : {adresse}")
        with lock:
            clients_connectes.append(connexion)

        # Attente synchronisée pour que tous les joueurs soient prêts
        with condition:
            if len(clients_connectes) < 2:
                send_to_player(connexion, "En attente d'autres joueurs...")
                condition.wait()  # Attendre que tous les joueurs soient prêts
            else:
                condition.notify_all()  # Notifier tous les clients lorsque 2 joueurs sont connectés

        # Notifier que la partie va commencer
        send_to_player(connexion, "La partie va commencer bientôt.")

        # Boucle principale pour le jeu
        while True:
            if connexion == clients_connectes[0]:  # Premier joueur (initiateur)
                send_to_player(connexion, "La partie commence !")
                game_loop()  # Démarrer la partie
                break
            else:
                # Maintenir le deuxième client connecté et en attente
                send_to_player(connexion, "En attente de votre tour...")
                with condition:  # Assurez-vous que le verrou est acquis
                    condition.wait()  # Attendre son tour
    except Exception as e:
        print(f"Erreur avec le client {adresse} : {e}")
    finally:
        with lock:
            if connexion in clients_connectes:
                clients_connectes.remove(connexion)
        connexion.close()
        print(f"Connexion fermée pour {adresse}")

def serveur_yahtzee():
    hote = '0.0.0.0'
    port = 12345
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.bind((hote, port))
    serveur_socket.listen(5)
    print(f"Serveur Yahtzee démarré sur {hote}:{port}")

    try:
        while True:
            connexion, adresse = serveur_socket.accept()
            threading.Thread(target=gerer_client, args=(connexion, adresse)).start()
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
    finally:
        serveur_socket.close()


if __name__ == "__main__":
    serveur_yahtzee()