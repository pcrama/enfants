# -*- coding: utf-8 -*-
from demineur import *

# Ces tests automatiques doivent aider à modifier demineur.py en ayant un peu
# moins peur de casser quelque chose.  Plus il est facile de tester que tout
# fonctionne encore, plus c'est facile de changer un programme: il suffit de
# faire le changement et de laisser les tests vérifier que tout fonctionne
# encore comme avant.  Bien sûr, ça ne fonctionne vraiment bien que si les
# tests automatisés vérifient tout.  Par exemple la fonction `jouer' dans
# demineur.py n'est pas testée ici et donc n'est pas "protégée".

def verifie(obtenu, attendu, s):
    if obtenu == attendu:
        return True
    else:
        raise Exception(f"{s}: j'ai eu {obtenu}, j'attendais {attendu}")

# Terrain de jeu de test
TABLEAU = [
   # colonne=0      colonne=1 colonne=2 colonne=3 colonne=4
    [INCONNU,       INCONNU,  BOMBE,    INCONNU,  INCONNU],       # rangée=0
    [BOMBE_DRAPEAU, INCONNU,  INCONNU,  INCONNU,  BOMBE_DRAPEAU], # rangée=1
    [INCONNU,       INCONNU,  INCONNU,  INCONNU,  INCONNU],       # rangée=2
    [INCONNU,       INCONNU,  DRAPEAU,  INCONNU,  INCONNU],       # rangée=3
    [BOMBE,         INCONNU,  BOMBE,    INCONNU,  INCONNU],       # rangée=4
]

def test_bombes_voisines():
    def verifie_bombes(rangee, colonne, valeur_attendue):
        verifie(bombes_voisines(TABLEAU, rangee, colonne),
                valeur_attendue,
                f"erreur dans bombes_voisines(t, {colonne}, {rangee})")
    verifie_bombes(0, 0, 1)
    verifie_bombes(0, 1, 2)
    verifie_bombes(2, 0, 1)
    verifie_bombes(0, 4, 1)
    verifie_bombes(1, 3, 2)
    verifie_bombes(2, 2, 0)
    verifie_bombes(4, 4, 0)
    verifie_bombes(3, 0, 1)
    verifie_bombes(4, 1, 2)

def test_cases_voisines():
    def verifie_voisins(rangee, colonne, valeur_attendue):
        # l'ordre des cases voisines n'a pas d'importance, donc nous trions
        # avec sorted(...) de la même facon la valeur obtenue et la valeur
        # attendue
        verifie(sorted(cases_voisines(TABLEAU, rangee, colonne)),
                sorted(valeur_attendue),
                f"erreur dans cases_voisines(TABLEAU, {colonne}, {rangee})")
    verifie_voisins(0, 0, [(0, 1), (1, 1), (1, 0)])
    verifie_voisins(0, 1, [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)])
    verifie_voisins(0, 4, [(0, 3), (1, 3), (1, 4)])
    verifie_voisins(0, 2, [(0, 1), (1, 1), (1, 2), (1, 3), (0, 3)])
    verifie_voisins(2, 2, [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)])
    verifie_voisins(4, 4, [(3, 4), (3, 3), (4, 3)])

def test_bombes_marquees():
    verifie(bombes_marquees(TABLEAU), 2, "erreur dans bombes_marquees(TABLEAU)")

def test_bombes_armees():
    verifie(bombes_armees(TABLEAU), 3, "erreur dans bombes_armees(TABLEAU)")

def test_drapeaux():
    verifie(drapeaux(TABLEAU), 3, "erreur dans drapeaux(TABLEAU)")

def tout_tester():
    test_bombes_marquees()
    test_bombes_armees()
    test_cases_voisines()
    test_bombes_voisines()
    test_drapeaux()

if __name__ == "__main__":
    tout_tester()
