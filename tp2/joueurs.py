# TP2 - Partie B : classes Joueur
# Toutes les classes ont la même méthode prochain_coup(tab, symbole) qui renvoie (x, y).
# Le jeu peut donc traiter un humain et une IA de la même manière (polymorphisme).
import random

from grille import cases_libres


class Joueur:
    """Classe de base : un joueur a un nom et sait choisir un coup."""

    def __init__(self, nom):
        self.nom = nom

    def prochain_coup(self, tab, symbole):
        # Chaque sous-classe doit redéfinir cette méthode
        raise NotImplementedError("À redéfinir dans la sous-classe")


class JoueurHumain(Joueur):
    """Joueur qui saisit son coup au clavier."""

    def prochain_coup(self, tab, symbole):
        while True:
            saisie = input(f"{self.nom} ({symbole}), ligne et colonne (ex : 1 2) : ")
            # On accepte "1 2" comme "1,2"
            morceaux = saisie.replace(",", " ").split()
            if len(morceaux) != 2:
                print("Tapez deux nombres séparés par un espace.")
                continue
            try:
                # On ne vérifie PAS ici que le coup est dans la grille ni libre :
                # c'est le rôle de Grille.jouer (le jeu redemande ensuite le coup).
                return int(morceaux[0]), int(morceaux[1])
            except ValueError:
                print("Entrez des nombres entiers.")


class JoueurIA(Joueur):
    """IA qui joue au hasard parmi les cases libres."""

    def __init__(self, nom="IA"):
        super().__init__(nom)

    def prochain_coup(self, tab, symbole):
        return random.choice(cases_libres(tab))


if __name__ == "__main__":
    # Petit test : l'IA choisit une case libre d'une grille presque pleine
    tab = [["X", "O", "X"], ["O", "X", "O"], ["O", " ", " "]]
    print(JoueurIA().prochain_coup(tab, "X"))  # (2, 1) ou (2, 2)
