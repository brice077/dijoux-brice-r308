# TP2 - Partie C : jeu complet du Morpion (+ bonus scores, 2 humains, IA maligne)
from grille import Grille
from ia_malin import JoueurIAMalin
from joueurs import JoueurHumain, JoueurIA


def partie(joueur_x, joueur_o, afficher=True):
    """Joue une partie. Renvoie le joueur gagnant, ou None en cas de match nul."""
    grille = Grille()
    joueurs = {"X": joueur_x, "O": joueur_o}
    symbole = "X"  # X commence

    while True:
        if afficher:
            print()
            grille.afficher()
        joueur = joueurs[symbole]

        # On redemande un coup tant qu'il est refusé : le même joueur rejoue
        # (Grille.jouer affiche déjà le message d'erreur)
        while True:
            x, y = joueur.prochain_coup(grille.tab, symbole)
            if grille.jouer(x, y, symbole):
                break

        # Victoire ?
        if grille.est_gagnant(symbole):
            if afficher:
                print()
                grille.afficher()
                print(f"\n{joueur.nom} ({symbole}) a gagné !")
            return joueur
        # Match nul ?
        if grille.est_plein():
            if afficher:
                print()
                grille.afficher()
                print("\nMatch nul.")
            return None
        # Sinon, au tour de l'autre joueur
        symbole = "O" if symbole == "X" else "X"


def demander_nom(defaut):
    return input(f"Nom ({defaut}) : ").strip() or defaut


def creer_joueurs(mode):
    """Construit les deux joueurs selon le mode choisi."""
    if mode == "1":
        return JoueurHumain(demander_nom("Joueur")), JoueurIA("IA")
    if mode == "2":
        return JoueurHumain(demander_nom("Joueur")), JoueurIAMalin("IA maligne")
    if mode == "3":
        j1 = JoueurHumain(demander_nom("Joueur 1"))
        j2 = JoueurHumain(demander_nom("Joueur 2"))
        if j2.nom == j1.nom:  # les scores sont indexés par nom : il faut des noms distincts
            j2.nom += " (2)"
        return j1, j2
    return JoueurIA("IA 1"), JoueurIA("IA 2")


def afficher_scores(scores):
    print("Scores : " + " | ".join(f"{nom} : {n}" for nom, n in scores.items()))


def main():
    print("1 = Humain contre IA")
    print("2 = Humain contre IA maligne")
    print("3 = Deux humains")
    print("4 = IA contre IA (20 parties)")
    mode = input("Mode : ").strip()
    j1, j2 = creer_joueurs(mode)
    scores = {j1.nom: 0, j2.nom: 0, "Nuls": 0}

    if mode not in ("1", "2", "3"):
        # Mode IA contre IA : 20 parties sans affichage
        for i in range(20):
            gagnant = partie(j1, j2, afficher=False)
            scores[gagnant.nom if gagnant else "Nuls"] += 1
        afficher_scores(scores)
        return

    numero = 0
    while True:
        # On alterne le joueur qui commence (celui qui a X) à chaque partie
        if numero % 2 == 0:
            gagnant = partie(j1, j2)
        else:
            gagnant = partie(j2, j1)
        numero += 1
        scores[gagnant.nom if gagnant else "Nuls"] += 1
        afficher_scores(scores)
        if input("Rejouer ? (o/n) : ").strip().lower() != "o":
            break


if __name__ == "__main__":
    main()
