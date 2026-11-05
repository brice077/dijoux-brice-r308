# TP3 - Partie A : classe Utilisateur (+ extension : limite d'emprunts)


class Utilisateur:
    # Extension : nombre maximum de livres empruntés en même temps
    # (mettre None pour supprimer la limite)
    LIMITE_EMPRUNTS = 3

    def __init__(self, nom):
        nom = str(nom).strip()
        if not nom:
            raise ValueError("Le nom ne peut pas être vide.")
        self.nom = nom
        self.emprunts = []  # liste d'objets Livre

    def emprunter_livre(self, livre):
        """Emprunte le livre. Renvoie True si réussi, False sinon (avec un message)."""
        if self.LIMITE_EMPRUNTS is not None and len(self.emprunts) >= self.LIMITE_EMPRUNTS:
            print(f"{self.nom} a déjà {self.LIMITE_EMPRUNTS} livres empruntés (limite atteinte).")
            return False
        # Le livre sait lui-même s'il est libre : on lui délègue la décision
        if livre.emprunter(self.nom):
            self.emprunts.append(livre)
            return True
        return False

    def rendre_livre(self, livre):
        """Rend un livre emprunté. Renvoie True si réussi, False sinon."""
        if livre not in self.emprunts:
            print(f"{self.nom} n'a pas emprunté « {livre.titre} ».")
            return False
        # On passe notre nom : le livre refuse si ce n'est pas nous l'emprunteur
        if livre.rendre(self.nom):
            self.emprunts.remove(livre)
            return True
        return False

    def afficher_emprunts(self):
        """Affiche la liste des livres empruntés."""
        if not self.emprunts:
            print(f"{self.nom} n'a aucun emprunt.")
            return
        print(f"Emprunts de {self.nom} :")
        for livre in self.emprunts:
            print(f"  - {livre.titre} ({livre.auteur})")


if __name__ == "__main__":
    from livre import Livre

    ana = Utilisateur("Ana")
    l1 = Livre("1984", "Orwell", 1949)
    print(ana.emprunter_livre(l1))  # True
    ana.afficher_emprunts()
    print(ana.rendre_livre(l1))     # True
    ana.afficher_emprunts()
