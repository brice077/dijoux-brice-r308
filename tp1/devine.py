# TP1 - Partie B : mini-jeu "Devine le nombre"
import random


def demander_entier(message):
    """Redemande une saisie tant que l'utilisateur ne tape pas un entier."""
    while True:
        try:
            return int(input(message))
        except ValueError:  # texte non numérique
            print("Entrez un nombre entier.")


def jouer(mini=1, maxi=100, essais_max=10):
    """Joue une partie. Renvoie True si le joueur gagne, False sinon."""
    secret = random.randint(mini, maxi)  # nombre secret, bornes incluses
    for essai in range(1, essais_max + 1):
        prop = demander_entier(f"Essai {essai}/{essais_max} - votre proposition ({mini}-{maxi}) : ")
        if prop < secret:
            print("Trop petit")
        elif prop > secret:
            print("Trop grand")
        else:
            print("Gagné")
            return True
    # Si la boucle se termine sans return, tous les essais sont utilisés
    print(f"Perdu, le nombre était {secret}")
    return False


def main():
    """Bonus : bornes personnalisables et possibilité de rejouer."""
    while True:
        choix = input("Bornes personnalisées ? (o/n) : ").strip().lower()
        if choix == "o":
            mini = demander_entier("Minimum : ")
            maxi = demander_entier("Maximum : ")
            if mini >= maxi:  # bornes incohérentes : on revient aux valeurs par défaut
                print("Bornes invalides, valeurs par défaut utilisées.")
                mini, maxi = 1, 100
        else:
            mini, maxi = 1, 100
        jouer(mini, maxi)
        if input("Rejouer ? (o/n) : ").strip().lower() != "o":
            break


if __name__ == "__main__":
    main()
