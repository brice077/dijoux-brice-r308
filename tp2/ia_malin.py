# TP2 - Bonus Jeu 1 : IA qui gagne si elle peut, sinon bloque l'adversaire, sinon hasard
from grille import cases_libres, gagne
from joueurs import JoueurIA


class JoueurIAMalin(JoueurIA):
    def __init__(self, nom="IA maligne"):
        super().__init__(nom)

    def _coup_gagnant(self, tab, symbole):
        """Renvoie une case qui fait gagner 'symbole' immédiatement, ou None."""
        for x, y in cases_libres(tab):
            # On teste sur une COPIE pour ne pas modifier la vraie grille
            copie = [ligne[:] for ligne in tab]
            copie[x][y] = symbole
            if gagne(copie, symbole):
                return (x, y)
        return None

    def prochain_coup(self, tab, symbole):
        adversaire = "O" if symbole == "X" else "X"
        # 1) Coup gagnant pour moi ?
        coup = self._coup_gagnant(tab, symbole)
        if coup:
            return coup
        # 2) Sinon, bloquer le coup gagnant de l'adversaire
        coup = self._coup_gagnant(tab, adversaire)
        if coup:
            return coup
        # 3) Sinon, hasard (méthode héritée de JoueurIA)
        return super().prochain_coup(tab, symbole)


# Jeux d'essai du sujet
if __name__ == "__main__":
    ia = JoueurIAMalin()
    # X X _ / _ O _ / _ _ _  -> O doit bloquer en (0, 2)
    print(ia.prochain_coup([["X", "X", " "], [" ", "O", " "], [" ", " ", " "]], "O"))
    # O O _ / X X _ / _ _ _  -> O doit gagner en (0, 2)
    print(ia.prochain_coup([["O", "O", " "], ["X", "X", " "], [" ", " ", " "]], "O"))
