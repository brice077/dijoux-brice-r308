# TP3 - Partie A : classe Livre


class Livre:
    def __init__(self, titre, auteur, annee, disponible=True, emprunteur=None):
        titre = str(titre).strip()
        auteur = str(auteur).strip()
        if not titre:
            raise ValueError("Le titre ne peut pas être vide.")
        self.titre = titre
        self.auteur = auteur
        # int() lève ValueError si l'année n'est pas un nombre : l'appelant gère l'erreur
        self.annee = int(annee)
        self.disponible = disponible
        self.emprunteur = emprunteur  # nom de l'emprunteur, None si le livre est disponible

    def __str__(self):
        etat = "disponible" if self.disponible else f"emprunté par {self.emprunteur}"
        return f"{self.titre} - {self.auteur} ({self.annee}) : {etat}"

    def afficher(self):
        """Affiche le livre sur une ligne."""
        print(self)

    def emprunter(self, nom):
        """Marque le livre comme emprunté par 'nom'.
        Renvoie True si l'emprunt réussit, False si le livre est déjà emprunté."""
        if not self.disponible:
            return False
        self.disponible = False
        self.emprunteur = nom
        return True

    def rendre(self, nom=None):
        """Rend le livre. Renvoie True si le retour réussit, False sinon.
        Si 'nom' est donné, seul l'emprunteur peut rendre le livre (cas piégé de la soutenance).
        Sans argument, le retour est accepté quel que soit l'emprunteur (jeu d'essai du sujet)."""
        if self.disponible:  # le livre n'est pas sorti : rien à rendre
            return False
        if nom is not None and nom != self.emprunteur:
            return False
        self.disponible = True
        self.emprunteur = None
        return True


# Jeu d'essai du sujet (s'exécute avec "python livre.py")
if __name__ == "__main__":
    l = Livre("1984", "Orwell", 1949)
    l.afficher()
    print(l.emprunter("Ana"))  # True
    print(l.emprunter("Léo"))  # False : déjà emprunté
    l.afficher()
    print(l.rendre())          # True
    l.afficher()
