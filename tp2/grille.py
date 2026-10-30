# TP2 - Partie A : classe Grille (plateau 3x3 du Morpion)
# Convention : dans jouer(x, y, joueur), x = numéro de LIGNE et y = numéro de COLONNE (0 à 2)

TAILLE = 3
VIDE = " "  # une case libre contient un espace


def gagne(tab, joueur):
    """True si 'joueur' a une ligne, une colonne ou une diagonale complète dans 'tab'.
    Fonction séparée de la classe pour que les IA puissent tester une grille quelconque."""
    for i in range(TAILLE):
        # ligne i complète ?
        if all(tab[i][j] == joueur for j in range(TAILLE)):
            return True
        # colonne i complète ?
        if all(tab[j][i] == joueur for j in range(TAILLE)):
            return True
    # diagonale descendante (0,0) (1,1) (2,2)
    if all(tab[i][i] == joueur for i in range(TAILLE)):
        return True
    # diagonale montante (0,2) (1,1) (2,0)
    if all(tab[i][TAILLE - 1 - i] == joueur for i in range(TAILLE)):
        return True
    return False


def cases_libres(tab):
    """Renvoie la liste des coups possibles [(x, y), ...] sur la grille 'tab'."""
    return [(x, y) for x in range(TAILLE) for y in range(TAILLE) if tab[x][y] == VIDE]


class Grille:
    def __init__(self):
        # Liste de listes : 3 lignes de 3 cases vides.
        # On écrit une compréhension (et non [[VIDE]*3]*3) pour que chaque ligne soit
        # une liste distincte : sinon modifier une ligne modifierait les 3.
        self.tab = [[VIDE] * TAILLE for _ in range(TAILLE)]

    def afficher(self):
        """Affiche la grille de façon lisible."""
        lignes = [" " + " | ".join(ligne) for ligne in self.tab]
        print("\n---------\n".join(lignes))

    def jouer(self, x, y, joueur):
        """Place 'X' ou 'O' en (x, y) si la case est libre.
        Renvoie True si le coup est joué, False s'il est refusé (avec un message)."""
        if joueur not in ("X", "O"):
            print("Coup refusé : le joueur doit être 'X' ou 'O'.")
            return False
        # Test explicite des bornes : sans lui, -1 serait accepté car Python
        # sait indexer depuis la fin d'une liste (tab[-1] = dernière ligne).
        if not (0 <= x < TAILLE and 0 <= y < TAILLE):
            print("Coup refusé : hors de la grille (valeurs de 0 à 2).")
            return False
        if self.tab[x][y] != VIDE:
            print("Coup refusé : case déjà occupée.")
            return False
        self.tab[x][y] = joueur
        return True

    def est_gagnant(self, j):
        """True si le joueur j a gagné."""
        return gagne(self.tab, j)

    def est_plein(self):
        """True si aucune case n'est libre."""
        return not cases_libres(self.tab)


# Jeu d'essai du sujet (s'exécute avec "python grille.py")
if __name__ == "__main__":
    g = Grille()
    g.jouer(0, 0, "X")
    g.jouer(0, 1, "O")
    g.jouer(1, 1, "X")
    g.afficher()
    print(g.jouer(0, 0, "O"))      # False : case occupée
    print(g.jouer(3, 0, "O"))      # False : hors grille
    print(g.est_gagnant("X"))      # False
    g.jouer(2, 2, "X")
    print(g.est_gagnant("X"))      # True (diagonale)
    print(g.est_plein())           # False
