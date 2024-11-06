import random

def gestion_du_game(nb_lancer_max):
    for i in range(1,nb_lancer_max+1):
        random_numbers = [random.randint(1, 6) for _ in range(6)]
        print(random_numbers)
        return random_numbers

gestion_du_game(1)