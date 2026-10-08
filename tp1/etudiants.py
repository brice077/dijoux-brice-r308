# TP1 - Partie A : dictionnaire d'étudiants
# Clé = nom (str), valeur = note (float)


def ajouter_etudiant(d, nom, note):
    """Ajoute un étudiant, ou met à jour sa note s'il existe déjà.
    Lève ValueError si la note n'est pas convertible en float."""
    # On remplace la virgule par un point pour accepter "12,5" comme "12.5"
    d[nom] = float(str(note).replace(",", "."))


def moyenne_classe(d):
    """Renvoie la moyenne des notes (0.0 si le dictionnaire est vide)."""
    if not d:  # évite une division par zéro
        return 0.0
    return sum(d.values()) / len(d)


def meilleur_etudiant(d):
    """Renvoie (nom, note) du meilleur étudiant, ou None si le dictionnaire est vide."""
    if not d:
        return None
    # max() sur les clés, en comparant leurs valeurs (les notes)
    nom = max(d, key=d.get)
    return (nom, d[nom])


def sauvegarder(d, chemin):
    """Écrit le dictionnaire dans un fichier texte, une ligne 'nom:note' par entrée.
    Renvoie True si tout s'est bien passé, False sinon."""
    try:
        with open(chemin, "w", encoding="utf-8") as f:
            for nom, note in d.items():
                f.write(f"{nom}:{note}\n")
        return True
    except OSError as e:  # dossier inexistant, droits insuffisants, disque plein...
        print(f"Erreur d'écriture ({chemin}) : {e}")
        return False


def charger(chemin):
    """Lit un fichier 'nom:note' et renvoie un dictionnaire.
    Ne plante pas si le fichier est absent ou si des lignes sont mal formées."""
    d = {}
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            for num, ligne in enumerate(f, 1):  # num = numéro de ligne (pour les messages)
                ligne = ligne.strip()
                if not ligne:  # on saute les lignes vides
                    continue
                # rpartition coupe au DERNIER ':' (le nom peut donc contenir ':')
                nom, sep, note = ligne.rpartition(":")
                if not sep or not nom.strip():  # pas de ':' ou nom vide
                    print(f"Ligne {num} ignorée (mal formée) : {ligne!r}")
                    continue
                try:
                    d[nom.strip()] = float(note.strip().replace(",", "."))
                except ValueError:  # la note n'est pas un nombre
                    print(f"Ligne {num} ignorée (note invalide) : {ligne!r}")
    except FileNotFoundError:
        print(f"Fichier {chemin} absent : départ avec un dictionnaire vide.")
    except OSError as e:
        print(f"Erreur de lecture ({chemin}) : {e}")
    return d


# Ce bloc ne s'exécute que si on lance directement "python etudiants.py"
# (pas quand un autre fichier fait "from etudiants import ...")
if __name__ == "__main__":
    # Jeu d'essai du sujet
    d = {}
    ajouter_etudiant(d, "Alice", 12)
    ajouter_etudiant(d, "Bob", 15)
    ajouter_etudiant(d, "Claire", 9.5)
    print(round(moyenne_classe(d), 2))  # attendu : 12.17
    print(meilleur_etudiant(d))         # attendu : ('Bob', 15.0)

    # Cas limite : dictionnaire vide
    print(moyenne_classe({}), meilleur_etudiant({}))

    # Sauvegarde puis rechargement
    sauvegarder(d, "notes.txt")
    print(charger("notes.txt"))

    # Cas limite : fichier absent
    print(charger("inexistant.txt"))

    # Cas limite : lignes mal formées
    with open("mauvais.txt", "w", encoding="utf-8") as f:
        f.write("Alice:12\nligne cassée\nBob:abc\n")
    print(charger("mauvais.txt"))  # attendu : {'Alice': 12.0}
