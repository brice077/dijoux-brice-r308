# TP1 - Partie C : manipulation des mots
import random

# Liste de secours si mots.txt est introuvable
MOTS_PAR_DEFAUT = ["python", "reseau", "serveur", "routeur"]


def charger_mots(chemin="mots.txt"):
    """Charge la liste de mots depuis un fichier texte (un mot par ligne)."""
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            # On enlève les espaces/retours à la ligne et on ignore les lignes vides
            mots = [ligne.strip() for ligne in f if ligne.strip()]
        return mots or MOTS_PAR_DEFAUT  # fichier vide -> liste par défaut
    except OSError:
        print(f"{chemin} introuvable : liste par défaut utilisée.")
        return MOTS_PAR_DEFAUT


def choisir_mot(liste):
    """Renvoie un mot tiré au hasard, en MAJUSCULES."""
    return random.choice(liste).upper()


def masque(mot):
    """Renvoie une liste de '_' de même longueur que le mot."""
    return ["_"] * len(mot)


if __name__ == "__main__":
    print(masque("PYTHON"))  # attendu : ['_', '_', '_', '_', '_', '_']
    print(choisir_mot(charger_mots()))
