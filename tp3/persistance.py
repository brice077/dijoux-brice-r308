# TP3 - Partie C : sauvegarde et chargement (CSV) + extension export JSON
# Ces fonctions prennent la bibliothèque en paramètre.
import csv
import json
import os

from bibliotheque import Bibliotheque
from livre import Livre
from utilisateur import Utilisateur

CHAMPS = ["titre", "auteur", "annee", "disponible", "emprunteur"]


def _ecrire_csv(chemin, champs, lignes):
    """Écrit un CSV de façon sûre : d'abord dans un fichier temporaire, puis on remplace.
    Si l'écriture plante en cours de route, l'ancien fichier reste intact."""
    temporaire = chemin + ".tmp"
    with open(temporaire, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)
    os.replace(temporaire, chemin)


def sauvegarder(biblio, chemin_livres="livres.csv", chemin_users="utilisateurs.csv"):
    """Sauvegarde les livres (titre, auteur, annee, disponible, emprunteur) et la liste
    des utilisateurs. Renvoie True si tout s'est bien passé, False sinon."""
    try:
        lignes = [
            {
                "titre": l.titre,
                "auteur": l.auteur,
                "annee": l.annee,
                "disponible": l.disponible,
                "emprunteur": l.emprunteur or "",  # vide si disponible
            }
            for l in biblio.livres.values()
        ]
        _ecrire_csv(chemin_livres, CHAMPS, lignes)
        # Fichier séparé pour les utilisateurs : sinon ceux qui n'ont aucun emprunt
        # seraient perdus au rechargement (on ne les verrait dans aucune ligne de livre).
        _ecrire_csv(chemin_users, ["nom"], [{"nom": nom} for nom in biblio.utilisateurs])
        return True
    except OSError as e:
        print(f"Erreur de sauvegarde : {e}")
        return False


def _lire_booleen(texte):
    """Convertit le texte du CSV en booléen. Lève ValueError si incompréhensible."""
    t = texte.strip().lower()
    if t in ("true", "1", "oui"):
        return True
    if t in ("false", "0", "non"):
        return False
    raise ValueError(f"booléen invalide : {texte!r}")


def charger(biblio, chemin_livres="livres.csv", chemin_users="utilisateurs.csv"):
    """Charge les données dans 'biblio' (son contenu actuel est remplacé).
    Renvoie True si le fichier des livres a été lu, False sinon (fichier absent...).
    Ne plante jamais : fichier absent, ligne mal formée, doublon -> message et on continue."""
    # 1) Lecture du fichier des livres dans une liste locale (biblio inchangée en cas d'échec)
    lignes = []
    try:
        with open(chemin_livres, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None or not set(CHAMPS) <= set(reader.fieldnames):
                print(f"{chemin_livres} : en-tête invalide, chargement annulé.")
                return False
            for ligne in reader:
                lignes.append((reader.line_num, ligne))
    except FileNotFoundError:
        print(f"Fichier {chemin_livres} absent : on démarre avec une bibliothèque vide.")
        return False
    except (OSError, csv.Error, UnicodeDecodeError) as e:
        print(f"Erreur de lecture de {chemin_livres} : {e}")
        return False

    # 2) Lecture des utilisateurs (si le fichier manque, ce n'est pas grave :
    #    les emprunteurs seront recréés à partir des livres)
    noms = []
    try:
        with open(chemin_users, "r", encoding="utf-8-sig", newline="") as f:
            noms = [l["nom"].strip() for l in csv.DictReader(f) if l.get("nom", "").strip()]
    except (OSError, csv.Error, UnicodeDecodeError):
        pass

    # 3) Reconstruction de la bibliothèque
    biblio.livres.clear()
    biblio.utilisateurs.clear()
    for nom in noms:
        biblio.ajouter_utilisateur(Utilisateur(nom))

    for num, ligne in lignes:
        try:
            titre = (ligne["titre"] or "").strip()
            disponible = _lire_booleen(ligne["disponible"] or "")
            emprunteur = (ligne["emprunteur"] or "").strip()
            if not disponible and not emprunteur:
                raise ValueError("livre emprunté sans emprunteur")
            # Livre() vérifie le titre et convertit l'année (ValueError si invalide)
            livre = Livre(titre, ligne["auteur"], ligne["annee"])
        except (ValueError, TypeError, KeyError) as e:
            print(f"Ligne {num} ignorée ({e}).")
            continue
        if not biblio.ajouter_livre(livre):  # doublon : message déjà affiché
            continue
        if not disponible:
            # On recrée l'emprunteur s'il n'existe pas, puis on relie le livre à lui
            if emprunteur not in biblio.utilisateurs:
                biblio.ajouter_utilisateur(Utilisateur(emprunteur))
            livre.disponible = False
            livre.emprunteur = emprunteur
            biblio.utilisateurs[emprunteur].emprunts.append(livre)
    return True


def exporter_json(biblio, chemin="livres.json"):
    """Extension : exporte livres et utilisateurs au format JSON. Renvoie True si réussi."""
    donnees = {
        "livres": [
            {
                "titre": l.titre,
                "auteur": l.auteur,
                "annee": l.annee,
                "disponible": l.disponible,
                "emprunteur": l.emprunteur,
            }
            for l in biblio.livres.values()
        ],
        "utilisateurs": [
            {"nom": u.nom, "emprunts": [l.titre for l in u.emprunts]}
            for u in biblio.utilisateurs.values()
        ],
    }
    try:
        with open(chemin, "w", encoding="utf-8") as f:
            # ensure_ascii=False garde les accents lisibles dans le fichier
            json.dump(donnees, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"Erreur d'export JSON : {e}")
        return False


# Jeu d'essai du sujet (s'exécute avec "python persistance.py")
if __name__ == "__main__":
    b = Bibliotheque()
    b.ajouter_livre(Livre("1984", "Orwell", 1949))
    b.ajouter_utilisateur(Utilisateur("Ana"))
    b.emprunter("Ana", "1984")
    print(sauvegarder(b, "test_livres.csv", "test_users.csv"))

    # Rechargement dans une NOUVELLE bibliothèque
    b2 = Bibliotheque()
    print(charger(b2, "test_livres.csv", "test_users.csv"))
    b2.livres["1984"].afficher()      # emprunté par Ana
    print(b2.rendre("Ana", "1984"))   # True : Ana peut le rendre
    print(charger(Bibliotheque(), "absent.csv"))  # False, sans plantage
    for f in ("test_livres.csv", "test_users.csv"):
        os.remove(f)
