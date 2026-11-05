# TP3 - Partie B : classe Bibliotheque
# (contient aussi les extensions : recherche par auteur, stats)


class Bibliotheque:
    def __init__(self):
        self.livres = {}        # dictionnaire titre -> Livre
        self.utilisateurs = {}  # dictionnaire nom -> Utilisateur

    # ----- Ajouts -----
    def ajouter_livre(self, livre):
        """Ajoute un livre. Refuse un titre déjà présent (le titre est la clé)."""
        if livre.titre in self.livres:
            print(f"Le livre « {livre.titre} » existe déjà.")
            return False
        self.livres[livre.titre] = livre
        return True

    def ajouter_utilisateur(self, utilisateur):
        """Ajoute un utilisateur. Refuse un nom déjà présent."""
        if utilisateur.nom in self.utilisateurs:
            print(f"L'utilisateur « {utilisateur.nom} » existe déjà.")
            return False
        self.utilisateurs[utilisateur.nom] = utilisateur
        return True

    # ----- Emprunts et retours -----
    def emprunter(self, nom, titre):
        """Fait emprunter le livre 'titre' par l'utilisateur 'nom'.
        Renvoie True si réussi, False sinon (message d'erreur, jamais de plantage)."""
        # .get() renvoie None si la clé n'existe pas (au lieu de lever KeyError)
        utilisateur = self.utilisateurs.get(nom)
        if utilisateur is None:
            print(f"Utilisateur inconnu : « {nom} ».")
            return False
        livre = self.livres.get(titre)
        if livre is None:
            print(f"Livre inconnu : « {titre} ».")
            return False
        if not livre.disponible:
            print(f"« {titre} » est déjà emprunté par {livre.emprunteur}.")
            return False
        return utilisateur.emprunter_livre(livre)

    def rendre(self, nom, titre):
        """Fait rendre le livre 'titre' par l'utilisateur 'nom'."""
        utilisateur = self.utilisateurs.get(nom)
        if utilisateur is None:
            print(f"Utilisateur inconnu : « {nom} ».")
            return False
        livre = self.livres.get(titre)
        if livre is None:
            print(f"Livre inconnu : « {titre} ».")
            return False
        if livre.disponible:
            print(f"« {titre} » n'est pas emprunté.")
            return False
        # Cas piégé : le livre est rendu par quelqu'un d'autre que l'emprunteur
        if livre.emprunteur != nom:
            print(f"« {titre} » est emprunté par {livre.emprunteur}, pas par {nom}.")
            return False
        return utilisateur.rendre_livre(livre)

    # ----- Affichage -----
    def afficher_livres(self):
        """Affiche les livres en deux groupes : disponibles puis empruntés."""
        dispos = [l for l in self.livres.values() if l.disponible]
        pris = [l for l in self.livres.values() if not l.disponible]
        print("Livres disponibles :")
        for l in dispos:
            print(f"  - {l.titre} ({l.auteur}, {l.annee})")
        if not dispos:
            print("  (aucun)")
        print("Livres empruntés :")
        for l in pris:
            print(f"  - {l.titre} ({l.auteur}, {l.annee}) -> {l.emprunteur}")
        if not pris:
            print("  (aucun)")

    # ----- Extensions -----
    def rechercher_par_auteur(self, auteur):
        """Renvoie la liste des livres dont l'auteur contient 'auteur'
        (sans tenir compte des majuscules, ni de la casse)."""
        motif = auteur.strip().casefold()
        return [l for l in self.livres.values() if motif and motif in l.auteur.casefold()]

    def stats(self):
        """Défi 1 : nombre de livres, d'emprunts et d'emprunts par utilisateur."""
        return {
            "total": len(self.livres),
            "empruntes": sum(1 for l in self.livres.values() if not l.disponible),
            # On ne garde que les utilisateurs qui ont au moins un emprunt
            "par_utilisateur": {
                nom: len(u.emprunts) for nom, u in self.utilisateurs.items() if u.emprunts
            },
        }


# Tests du sujet et cas piégés (s'exécute avec "python bibliotheque.py")
if __name__ == "__main__":
    from livre import Livre
    from utilisateur import Utilisateur

    b = Bibliotheque()
    b.ajouter_livre(Livre("1984", "Orwell", 1949))
    b.ajouter_livre(Livre("Dune", "Herbert", 1965))
    b.ajouter_livre(Livre("La Ferme des animaux", "Orwell", 1945))
    b.ajouter_utilisateur(Utilisateur("Ana"))
    b.ajouter_utilisateur(Utilisateur("Léo"))

    print(b.emprunter("Ana", "1984"))        # True
    print(b.emprunter("Léo", "1984"))        # False : déjà emprunté
    print(b.emprunter("Zoe", "Dune"))        # False : utilisateur inconnu
    print(b.emprunter("Ana", "Inconnu"))     # False : livre inconnu
    print(b.rendre("Léo", "1984"))           # False : pas l'emprunteur
    b.emprunter("Ana", "Dune")
    b.afficher_livres()
    print(b.stats())
    print(b.rendre("Ana", "1984"))           # True
    print([l.titre for l in b.rechercher_par_auteur("orwell")])
