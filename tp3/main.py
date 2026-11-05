# TP3 - Partie D : programme principal (menu texte interactif)
import os

import persistance
from bibliotheque import Bibliotheque
from livre import Livre
from utilisateur import Utilisateur

# Les fichiers sont rangés à côté du script, quel que soit le dossier depuis lequel on lance
DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_LIVRES = os.path.join(DOSSIER, "livres.csv")
FICHIER_USERS = os.path.join(DOSSIER, "utilisateurs.csv")
FICHIER_JSON = os.path.join(DOSSIER, "livres.json")

MENU = """
===== Bibliothèque =====
1 - Ajouter un livre
2 - Ajouter un utilisateur
3 - Emprunter un livre
4 - Rendre un livre
5 - Afficher les livres
6 - Quitter et sauvegarder
7 - Statistiques
8 - Rechercher par auteur
0 - Exporter en JSON"""


def demander(message):
    return input(message).strip()


def ajouter_livre(biblio):
    titre = demander("Titre : ")
    auteur = demander("Auteur : ")
    annee = demander("Année : ")
    try:
        livre = Livre(titre, auteur, annee)  # lève ValueError si titre vide ou année non numérique
    except ValueError:
        # Message volontairement général : couvre l'année invalide et le titre vide
        print("Données invalides : le titre est obligatoire et l'année doit être un nombre entier.")
        return
    if biblio.ajouter_livre(livre):
        print("Livre ajouté.")


def ajouter_utilisateur(biblio):
    try:
        utilisateur = Utilisateur(demander("Nom : "))
    except ValueError as e:
        print(e)
        return
    if biblio.ajouter_utilisateur(utilisateur):
        print("Utilisateur ajouté.")


def emprunter(biblio):
    nom = demander("Nom de l'utilisateur : ")
    titre = demander("Titre du livre : ")
    if biblio.emprunter(nom, titre):
        print("Emprunt enregistré.")


def rendre(biblio):
    nom = demander("Nom de l'utilisateur : ")
    titre = demander("Titre du livre : ")
    if biblio.rendre(nom, titre):
        print("Retour enregistré.")


def rechercher(biblio):
    resultats = biblio.rechercher_par_auteur(demander("Auteur : "))
    if not resultats:
        print("Aucun livre trouvé.")
    for livre in resultats:
        livre.afficher()


def statistiques(biblio):
    print(biblio.stats())


def exporter(biblio):
    if persistance.exporter_json(biblio, FICHIER_JSON):
        print(f"Export JSON écrit dans {FICHIER_JSON}")


def sauvegarder(biblio):
    """Sauvegarde ; renvoie True si on peut quitter."""
    if persistance.sauvegarder(biblio, FICHIER_LIVRES, FICHIER_USERS):
        print("Données sauvegardées. Au revoir.")
        return True
    # Sauvegarde échouée : on ne quitte pas sans demander (sinon les données seraient perdues)
    return demander("Sauvegarde impossible. Quitter quand même ? (o/n) : ").lower() == "o"


def main():
    biblio = Bibliotheque()
    # Au lancement : on recharge l'état précédent (fichier absent -> message, bibliothèque vide)
    persistance.charger(biblio, FICHIER_LIVRES, FICHIER_USERS)

    # Dictionnaire choix -> fonction : plus lisible qu'une longue suite de if/elif
    actions = {
        "1": ajouter_livre,
        "2": ajouter_utilisateur,
        "3": emprunter,
        "4": rendre,
        "5": lambda b: b.afficher_livres(),
        "7": statistiques,
        "8": rechercher,
        "0": exporter,
    }

    try:
        while True:
            print(MENU)
            choix = demander("Votre choix : ")
            if choix == "6":
                if sauvegarder(biblio):
                    break
            elif choix in actions:
                actions[choix](biblio)
            else:
                print("Choix invalide.")
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C ou fin de l'entrée : on sauvegarde quand même pour ne rien perdre
        print("\nInterruption : sauvegarde en cours...")
        persistance.sauvegarder(biblio, FICHIER_LIVRES, FICHIER_USERS)


if __name__ == "__main__":
    main()
