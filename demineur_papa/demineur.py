# -*- coding: utf-8 -*-
import random

# Le but du jeu est de déminer chaque endroit, soit en plantant un drapeau
# pour avertir qu'il pourrait y avoir une bombe, soit en "marchant" dessus:
# soit il y avait une bombe et le jeu est terminé, ou alors on apprend combien
# de bombes sont autour de l'endroit.
#
# Le jeu sera représenté par un tableau à deux entrées: la rangée (la ligne)
# et la colonne, numérotés à partir de 0.  Par exemple,
#
#    case(terrain_de_jeu, 0, 3)
#
# est marqué par un X ci-dessous
#
#      0   1   2   3   4
#    +---+---+---+---+---+
#  0 |   |   |   | X |   |
#    +---+---+---+---+---+
#  1 |   |   |   |   |   |
#    +---+---+---+---+---+
#  2 |   |   |   |   |   |
#    +---+---+---+---+---+
#  3 |   |   |   |   |   |
#    +---+---+---+---+---+
#  4 |   |   |   |   |   |
#    +---+---+---+---+---+
#
# Chaque case dans le tableau est un endroit que l'on peut déminer.  Elles
# sont initialisées avec la valeur INCONNU ou BOMBE.  Au fur et à mesure que
# le joueur les démine ou plante des drapeaux, chaque case est remplie avec le
# nombre de bombes qui l'entourent (un nombre positif entre 0 et 8, bornes
# comprises, raison pour laquelle les constantes INCONNU, BOMBE, BOMBE_DRAPEAU
# et DRAPEAU sont négatives).
#
# Améliorations possibles
#
# 1. Limiter le nombre de drapeaux: empêcher de planter plus de drapeaux qu'il
#    n'y a de bombes au total.
# 2. Changer la taille du terrain de jeu et/ou le nombre de bombes
# 3. Permettre de retirer un drapeau qu'on a planté.
# 4. Un affichage graphique plutôt que texte (Chapître 12 de "Python pour les
#    Kids")

INCONNU = -1 # la case n'a pas encore été déminée, mais il n'y a pas de bombe
BOMBE = -2 # la case n'a pas encore été déminée, mais il y a une bombe!
BOMBE_DRAPEAU = -3 # le joueur a planté un drapeau correctement (il y a une bombe en dessous)
DRAPEAU = -4 # le joueur a planté un drapeau en erreur (il n'y a pas de bombe en dessous)

def nouveau_jeu():
    "Crée un nouveau jeu avec des bombes placées au hasard et toutes les autres cases vides"
    # Nous commen‌çons par un tableau où toutes les cases sont vides ...
    tableau = [[INCONNU, INCONNU, INCONNU, INCONNU, INCONNU]
               for _rangee in range(5)]
    # ... puis nous ajoutons les bombes.  Nous essayons de placer autant de
    # bombes que de rangées, mais on peut avoir "pas de chance" et mettre une
    # bombe dans une case où il y en avait déjà une: dans ce cas, c'est comme
    # si il y avait une bombe en moins.
    for bombe in range(len(tableau)):
        # p.ex. random.randrange(5) peut être 0, 1, 2, 3 ou 4 (au hasard)
        tableau[random.randrange(rangees(tableau))][random.randrange(colonnes(tableau))] = BOMBE
    return tableau

def case(terrain_de_jeu, rangee, colonne):
    return terrain_de_jeu[rangee][colonne]

def rangees(terrain_de_jeu):
    "Compte le nombre de rangées dans le jeu"
    return len(terrain_de_jeu)

def colonnes(terrain_de_jeu):
    "Compte le nombre de colonnes dans le jeu"
    return len(terrain_de_jeu[0])

def bombes_marquees(terrain_de_jeu):
    """Compte le nombre de drapeaux placés correctement dans le jeu

    Un drapeau est placé correctement seulement si il y a une bombe en
    dessous."""
    # sum(i*j for i in range(2) for j in range(5, 7)) = 0*5 + 1*5 + 0*6 + 1*6
    return sum(1 if case(terrain_de_jeu, rangee, colonne) == BOMBE_DRAPEAU else 0
               for colonne in range(colonnes(terrain_de_jeu))
               for rangee in range(rangees(terrain_de_jeu)))

def bombes_armees(terrain_de_jeu):
    """Compte le nombre de bombes qui n'ont pas encore été déminées

    Une bombe sans drapeau au dessus n'a pas encore été déminée."""
    # sum(i*j for i in range(2) for j in range(5, 7)) = 0*5 + 1*5 + 0*6 + 1*6
    return sum(1 if case(terrain_de_jeu, rangee, colonne) == BOMBE else 0
               for colonne in range(colonnes(terrain_de_jeu))
               for rangee in range(rangees(terrain_de_jeu)))

def cases_voisines(terrain_de_jeu, rangee, colonne):
    """Liste des cases voisines d'une case donnée

    Chaque case dans la liste est représentée par un tuple: (rangée, colonne).

    Une case a au moins 3 voisins (pour les cases du coins), parfois 5 voisins
    (celles qui sont sur le bord mais pas dans un coin), ou alors 8 voisins
    (toutes celles qui ne sont pas sur le bord).

             0   1   2   3   4
           +---+---+---+---+---+
         0 |   |   | x | X | x | Les 5 cases voisines de `X' sont marquées
           +---+---+---+---+---+ avec `x': [(0,2),(0,4),(1,2),(1,3),(1,4)]
         1 |   |   | x | x | x |
           +---+---+---+---+---+
         2 | a | a | a |   |   |
           +---+---+---+---+---+ Les 8 cases voisines de `A' sont marquées
         3 | a | A | a |   |   | avec `a': [(2,0),(2,1),(2,2),(3,0),(3,2),
           +---+---+---+---+---+ (4,0),(4,1),(4,2)]
         4 | a | a | a |   |   |
           +---+---+---+---+---+"""
    return [(autre_rangee, autre_colonne)
            for autre_colonne in range(colonne - 1, colonne + 2)
            for autre_rangee in range(rangee - 1, rangee + 2)
            if (autre_colonne >= 0) and (autre_rangee >= 0) and
               (autre_colonne < colonnes(terrain_de_jeu)) and (autre_rangee < rangees(terrain_de_jeu)) and
               ((autre_colonne != colonne) or (autre_rangee != rangee))]

def drapeaux(terrain_de_jeu):
    """Compte le nombre de drapeaux déjà placés

    Tous les drapeaux sont pris en compte, même si ils ne sont pas placés au
    dessus d'une bombe."""
    # 0 in [0, 1] est vrai parce que 0 est dans la liste; 3 in [0, 4] est faux
    # par contre: 3 n'est pas un élément de la liste (en d'autres mots, 3
    # n'est ni 0, ni 4).
    return sum(1 if case(terrain_de_jeu, rangee, colonne) in [DRAPEAU, BOMBE_DRAPEAU]
               else 0
               for rangee in range(0, rangees(terrain_de_jeu))
               for colonne in range(0, colonnes(terrain_de_jeu)))

def bombes_voisines(terrain_de_jeu, rangee, colonne):
    """Compte le nombre de bombes autour d'une case donnée (cf. cases_voisines)

    Toute les bombes sont prises en compte, même si elles sont déjà marquées
    par un drapeau."""
    # 0 in [0, 1] est vrai parce que 0 est dans la liste; 3 in [0, 4] est faux
    # par contre: 3 n'est pas un élément de la liste (en d'autres mots, 3
    # n'est ni 0, ni 4).
    return sum(1 if case(terrain_de_jeu, autre_rangee, autre_colonne) in [BOMBE, BOMBE_DRAPEAU]
               else 0
               for (autre_rangee, autre_colonne) in cases_voisines(terrain_de_jeu, rangee, colonne))

def montre_le_terrain(terrain_de_jeu):
    """Affiche le terrain"""
    # 1. D'abord imprimer les coordonnées pour repérer les colonnes
    for colonne in range(0, colonnes(terrain_de_jeu)):
        print(f' {colonne:2} ', end='') # end='' veut dire de ne pas aller à la ligne après
    print('') # aller à la ligne une fois que tous les numéros de colonne ont été imprimés
    # 2. Puis, pour chaque rangée, ...
    for rangee in range(0, rangees(terrain_de_jeu)):
        # ... imprimer toutes les colonnes ...
        for colonne in range(0, colonnes(terrain_de_jeu)):
            if case(terrain_de_jeu, rangee, colonne) in [BOMBE, INCONNU]:
                print(" ?? ", end='')
            elif case(terrain_de_jeu, rangee, colonne) in [DRAPEAU, BOMBE_DRAPEAU]:
                print(" DD ", end='')
            elif case(terrain_de_jeu, rangee, colonne) >= 0:
                print("  {} ".format(bombes_voisines(terrain_de_jeu, rangee, colonne)), end='')
            else:
                print("PROBLEME, on ne devrait pas se retrouver ici")
        # ... puis le numéro de la rangée pour aider le joueur à se
        # repérer et aller à la ligne (pas de end='')
        print(f"| rangee={rangee:2}")

def demine(terrain_de_jeu, rangee, colonne):
    """Marcher dans une case

    La fonction retourne vrai (True) si le jeu peut continuer, et faux (False)
    si le jeu doit s'arrêter parce que une bombe a explosé."""
    if case(terrain_de_jeu, rangee, colonne) in [DRAPEAU, BOMBE_DRAPEAU]:
        # Protéger le joueur: si il a planté un drapeau, c'est qu'il croit
        # qu'il y a une bombe et donc ne pas le laisser marcher sur cette
        # case:
        print("Il y a deja un drapeau")
        return True
    elif case(terrain_de_jeu, rangee, colonne) == BOMBE:
        # Le joueur a perdu!
        print("BOUM BOUM BOUM")
        return False
    elif case(terrain_de_jeu, rangee, colonne) == INCONNU:
        bombes_tout_pres = bombes_voisines(terrain_de_jeu, rangee, colonne)
        # Marque la case comme étant déminée
        terrain_de_jeu[rangee][colonne] = bombes_tout_pres
        # Pour aider le joueur, si une case n'a pas de bombes autour, ...
        if bombes_tout_pres == 0:
            # ... nous déminons automatiquement toutes les cases voisines ...
            for (autre_rangee, autre_colonne) in cases_voisines(
                    terrain_de_jeu, rangee, colonne):
                # ... qui n'ont pas encore été déminées, puisqu'il n'y a aucun
                # danger.
                #
                # Note que ne déminer que les cases qui sont encore inconnues
                # empêchent une boucle infinie parce que nous avons déjà
                # marqué la première case comme déminée.
                if case(terrain_de_jeu, autre_rangee, autre_colonne) == INCONNU:
                    demine(terrain_de_jeu, autre_rangee, autre_colonne)
        return True
    else:
        # Le joueur avait déjà marché sur cette case, il n'y a rien à changer,
        # mais aucun danger non plus:
        return True

def plante_drapeau(terrain_de_jeu, rangee, colonne):
    "Met un drapeau sur une case donnée pour indiquer que le joueur soupçonne une bombe"
    if case(terrain_de_jeu, rangee, colonne) in [DRAPEAU, BOMBE_DRAPEAU]:
        print("Il y a deja un drapeau")
    elif case(terrain_de_jeu, rangee, colonne) == BOMBE:
        terrain_de_jeu[rangee][colonne] = BOMBE_DRAPEAU
    elif case(terrain_de_jeu, rangee, colonne) == INCONNU:
        terrain_de_jeu[rangee][colonne] = DRAPEAU
    else:
        print("Endroit deja déminé")

def oui_ou_non(question):
    """Pose une question jusqu'à ce que le joueur réponde O pour oui ou N pour non

    La fonction retourne vrai (True) si la réponse était oui"""
    # Une boucle infinie dont nous ne sortirons avec `return ...' uniquement
    # si nous avons une réponse qui nous convient:
    while True:
        reponse = input(question).upper()
        if reponse in "ON":
            return reponse == 'O'

def demande_nombre(question, minimum, maximum):
    """Pose un question jusqu'à ce que le joueur réponde par un nombre entier dans la fourchette

    La fourchette est [minimum, maximum), c'est à dire que la borne inférieure
    fait partie de la fourchette, mais pas la borne supérieure."""
    # Une boucle infinie dont nous ne sortirons avec `return ...' uniquement
    # si nous avons une réponse qui nous convient:
    while True:
        reponse = input(question)
        try:
            # Essayons de transformer la chaîne de caractères en un nombre entier ...
            nombre = int(reponse)
        except Exception:
            # ... Possibilité 1: ce n'était pas un nombre entier (p.ex. blabla ou 3.14)
            pass
        else:
            # ... Possibilité 2: c'est un nombre entier ...
            if minimum <= nombre < maximum:
                # ... et dans la bonne fourchette, quittons la boucle et
                # renvoyons la réponse
                return nombre
            else:
                # ... mais pas dans la bonne fourchette, ne faisons rien de
                # spécial, c'est à dire, continuons la boucle
                #
                # Note que les lignes `else: pass' n'étaient pas strictement
                # nécessaires, je les inclus uniquement pour pouvoir places ce
                # commentaire.
                pass

def jouer(terrain_de_jeu):
    "Joue un partie sur un terrain donné"
    fini = False
    perdu = False
    # Tant que le jeu n'est pas fini (toutes les cases remplies) ou perdu (une
    # bombe a explosé):
    while not (fini or perdu):
        # 1. Montre l'état actuel du jeu
        montre_le_terrain(terrain_de_jeu)
        print("Il y a {} bombes et {} drapeaux".format(
            bombes_armees(terrain_de_jeu) + bombes_marquees(terrain_de_jeu),
            drapeaux(terrain_de_jeu)))
        # 2. Demande au joueur ce qu'il veut faire
        planter_drapeau = oui_ou_non("Drapeau (O/N)? ")
        rangee = demande_nombre("Rangee? ", 0, rangees(terrain_de_jeu))
        colonne = demande_nombre("Colonne? ", 0, colonnes(terrain_de_jeu))
        # 3. Fais ce qu'il t'a demandé
        if planter_drapeau:
            plante_drapeau(terrain_de_jeu, rangee, colonne)
        else:
            # Quand on démine une case, on risque toujours de perdre:
            perdu = not demine(terrain_de_jeu, rangee, colonne)
        # Vérifier si le jeu n'est pas fini parce que toutes les cases sont
        # remplies:
        fini = not any(case(terrain_de_jeu, rangee, colonne) in [INCONNU, BOMBE]
                       for rangee in range(0, rangees(terrain_de_jeu))
                       for colonne in range(0, colonnes(terrain_de_jeu)))
    if fini and not perdu:
        print("Bravo!")

def partie():
    "Crée une nouvelle partie et laisse le joueur jouer"
    terrain_de_jeu = nouveau_jeu()
    jouer(terrain_de_jeu)
