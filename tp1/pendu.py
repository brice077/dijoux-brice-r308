# TP1 - Partie D : jeu du Pendu (+ bonus hall of fame et tournoi)
from getpass import getpass  # saisie masquée (pour le mot du voisin)

from etudiants import charger, sauvegarder  # réutilisés pour lire/écrire scores.txt
from mots import charger_mots, choisir_mot, masque

MAX_ERREURS = 7


def jouer_pendu(mot):
    """Joue une partie sur le mot donné. Renvoie True si gagné, False si perdu."""
    mot = mot.upper()        # gère "Python", "ÉLÉPHANT"... sans plantage
    m = masque(mot)          # mot masqué, ex. ['_', '_', '_']
    erreurs = 0
    proposees = []           # lettres déjà proposées

    # On continue tant qu'il reste des '_' et que le joueur n'a pas atteint 7 erreurs
    while "_" in m and erreurs < MAX_ERREURS:
        print()
        print(" ".join(m))
        print(f"Erreurs : {erreurs}/{MAX_ERREURS}")
        print(f"Lettres proposées : {', '.join(proposees) if proposees else '-'}")

        lettre = input("Une lettre : ").strip().upper()

        # Validation : exactement une lettre
        if len(lettre) != 1 or not lettre.isalpha():
            print("Entrez une seule lettre.")
            continue
        # Lettre déjà jouée : aucune pénalité
        if lettre in proposees:
            print("Lettre déjà proposée.")
            continue

        proposees.append(lettre)
        if lettre in mot:
            # Lettre présente : on révèle toutes ses positions dans le masque
            for i, c in enumerate(mot):
                if c == lettre:
                    m[i] = lettre
        else:
            # Lettre absente : une erreur de plus
            erreurs += 1

    # Fin de partie : victoire s'il n'y a plus de '_'
    if "_" not in m:
        print(f"\n{' '.join(m)}\nGagné")
        return True
    print(f"\nPerdu, le mot était {mot}")
    return False


def mot_du_voisin():
    """Tournoi : demande un mot sans l'afficher à l'écran (le voisin ne doit pas le voir)."""
    while True:
        mot = getpass("Mot pour votre voisin (saisie masquée) : ").strip()
        if mot.isalpha():
            return mot
        print("Le mot doit contenir uniquement des lettres.")


def main():
    # Hall of fame : on relit les scores (absent -> dictionnaire vide, départ à zéro)
    scores = charger("scores.txt")
    nom = input("Votre nom : ").strip() or "Anonyme"

    while True:
        mode = input("Mode : 1 = mot aléatoire, 2 = mot choisi par un voisin : ").strip()
        mot = mot_du_voisin() if mode == "2" else choisir_mot(charger_mots())

        if jouer_pendu(mot):
            # Victoire : +1 au score du joueur (float pour obtenir "Ana:2.0")
            scores[nom] = scores.get(nom, 0.0) + 1
        print(f"\nVictoires de {nom} : {scores.get(nom, 0.0)}")

        if input("Rejouer ? (o/n) : ").strip().lower() != "o":
            break

    # Réécriture des scores à la fin
    sauvegarder(scores, "scores.txt")


if __name__ == "__main__":
    main()
