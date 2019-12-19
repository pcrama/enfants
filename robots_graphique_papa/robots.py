# -*- coding: utf-8 -*-
import random
from tkinter import (Tk, Canvas, ALL)

# Dans les commentaires, l'abbréviation PplK signifie "Python pour les Kids"
# et renvoit à des explications dans ce livre.
#
# Le but du jeu est de ne pas se faire attraper par les robots meurtriers.
# Les robots sont fragiles et primitifs: à la moindre collision, ils se
# cassent et ils suivent toujours le plus court chemin vers le joueur, même si
# ça veut dire qu'ils se cassent.  À chaque tour, le joueur bouge, puis tous
# les robots bougent ensemble.  Si il y a une collision entre robots, les
# débris forment un nouvel obstacle.  Le joueur peut choisir de passer son
# tour ou de bouger dans 8 directions (nord = haut, nord-est = en haut et à
# droite, est = droite etc.)
#
# Le terrain de jeu est représenté comme tableau à double entrée: la rangée et
# la colonne.

VIDE = 0 # la case est vide et peut être utilisée par un robot ou un joueur
JOUEUR = 1 # pour repérer le joueur (il n'y en a que un!)
ROBOT = 2 # pour repérer les robots (il peut y en avoir plusieurs)
OBSTACLE = 3 # pour empêcher de sortir du terrain de jeu ou pour marquer les débris de robots entrés en collision

TAILLE_CASE = 30 # chaque case est dessinée avec un carré de ... pixels de côté

def nouveau_jeu():
    "Crée un nouveau terrain de jeu"
    # Dimensions du terrain de jeu (compté en cases)
    COLONNES = 30
    RANGEES = 18
    # Commençons avec un tableau vide ...
    tableau = [[VIDE] * COLONNES for _r in range(RANGEES)]
    # ... entouré par des obstacles (en haut et en bas du tableau) ...
    for colonne in range(COLONNES):
        tableau[0][colonne] = OBSTACLE
        tableau[RANGEES - 1][colonne] = OBSTACLE
    # ... entouré par des obstacles (à gauche et à droite du tableau)
    for rangee in range(RANGEES):
        tableau[rangee][0] = OBSTACLE
        tableau[rangee][COLONNES - 1] = OBSTACLE
    # Plaçons le joueur (pas trop près du bord):
    # p.ex. random.randrange(6, 18 - 6) = 6, 7, 8, 9, 10 ou 11 (au hasard, PplK 176)
    rangee_joueur = random.randrange(6, RANGEES - 6)
    colonne_joueur = random.randrange(6, COLONNES - 6)
    tableau[rangee_joueur][colonne_joueur] = JOUEUR
    # Plaçons les robots:
    ROBOTS = 15 # combien de robots il faut placer en tout.
    # Nous allons essayer de placer un nouveau robot aussi longtemps qu'il n'y
    # en a pas assez (PplK 81 et 311):
    while robots(tableau) < ROBOTS:
        # Choisissons une place au hasard en évitant les obstacles qui
        # entourent le terrain de jeu ...
        rangee = random.randrange(1, RANGEES - 1)
        colonne = random.randrange(1, COLONNES - 1)
        # ... et en ne nous mettant pas trop près du joueur. `abs' rend un
        # nombre positif, p.ex. abs(-3) = 3 et abs(4) = 4 (PplK 114); cela
        # permet de calculer la distance de (rangee, colonne) par rapport au
        # joueur:
        if (abs(rangee - rangee_joueur) + abs(colonne - colonne_joueur)
            # La distance initiale entre les robots et le joueur dépend de la
            # taille du terrain:
            > (min(RANGEES, COLONNES) // 3)): # p.ex. min(3, 1, 2) = 1 (PplK 122-123)
            tableau[rangee][colonne] = ROBOT
    # Mettons aussi quelques obstacles pour que le joueur puisse se cacher.
    # Nous utilisons une boucle for (PplK 73 et 304) parce que le nombre de
    # fois que nous voulons essayer de placer un obstacle est décidé à
    # l'avance:
    for _ in range(min(COLONNES, RANGEES) // 2):
        # Choisissons une place au hasard en évitant les obstacles qui
        # entourent le terrain de jeu
        rangee = random.randrange(1, RANGEES - 1)
        colonne = random.randrange(1, COLONNES - 1)
        # si la case est encore vide, on peut mettre un obstacle
        if case(tableau, rangee, colonne) == VIDE:
            tableau[rangee][colonne] = OBSTACLE
    return tableau

def rangees(terrain_de_jeu):
    "Nombre de rangées dans le terrain de jeu"
    return len(terrain_de_jeu)

def colonnes(terrain_de_jeu):
    "Nombre de colonnes dans le terrain de jeu"
    return len(terrain_de_jeu[0])

def case(terrain_de_jeu, rangee, colonne):
    return terrain_de_jeu[rangee][colonne]

def robots(terrain_de_jeu):
    "Compte le nombre de robots présents sur le terrain de jeu"
    # p.ex. sum([1, 1, 1]) = 3 (PplK 125)
    return sum(1
               # parcourt toutes les rangées
               for rangee in range(rangees(terrain_de_jeu))
               # et pour toutes les rangées, parcourt toutes les colonnes
               for colonne in range(colonnes(terrain_de_jeu))
               # [i for i in [1, 2, 3, 1, 2] if i > 1] = [2, 3, 2]
               if case(terrain_de_jeu, rangee, colonne) == ROBOT)

def montre_joueur(canvas, x_origine, y_origine):
    "Dessine le joueur sur le canevas"
    cou_y = y_origine + TAILLE_CASE // 3
    droite_x = x_origine + TAILLE_CASE - 1
    bifurcum_x = x_origine + TAILLE_CASE // 2
    bifurcum_y = y_origine + (2 * TAILLE_CASE) // 3
    pied_y = y_origine + TAILLE_CASE - 1
    # Tête
    canvas.create_oval(x_origine + TAILLE_CASE // 3, y_origine,
                       x_origine + (2 * TAILLE_CASE) // 3, cou_y)
    # Bras
    canvas.create_line(x_origine, cou_y, droite_x, cou_y)
    # Tronc
    canvas.create_line(bifurcum_x, cou_y, bifurcum_x, bifurcum_y)
    # 2 jambes:
    canvas.create_line(x_origine, pied_y, bifurcum_x, bifurcum_y)
    canvas.create_line(droite_x, pied_y, bifurcum_x, bifurcum_y)

def montre_obstacle(canvas, x_origine, y_origine):
    "Dessine un obstacle sur le canvas"
    canvas.create_rectangle(x_origine, y_origine,
                            x_origine + TAILLE_CASE - 1, y_origine + TAILLE_CASE - 1,
                            fill='black')

def montre_robot(canvas, x_origine, y_origine):
    "Dessine un robot sur le canvas"
    droite_x = x_origine + TAILLE_CASE - 1
    cou_y = y_origine + TAILLE_CASE // 2
    bifurcum_y = y_origine + (3 * TAILLE_CASE) // 4
    pied_y = y_origine + TAILLE_CASE - 1
    COULEUR = 'red' # rouge
    # Tête
    canvas.create_oval(x_origine, y_origine + 1, droite_x, cou_y,
                       outline=COULEUR, fill=COULEUR)
    # Corps
    canvas.create_rectangle(x_origine, cou_y, droite_x, bifurcum_y,
                            outline=COULEUR, fill=COULEUR)
    # 2 jambes:
    canvas.create_line(x_origine, pied_y, x_origine, bifurcum_y, fill=COULEUR)
    canvas.create_line(droite_x, pied_y, droite_x, bifurcum_y, fill=COULEUR)

def montre_le_terrain(terrain_de_jeu, canvas):
    canvas.delete(ALL) # efface tout avant de re-dessiner au-dessus dessiner
    # les commandes: un carré de 3x3 `boutons', chaque bouton représentant une
    # direction et le bouton du centre signifiant que le joueur veut passer
    # son tour.
    #
    # Si ça paraît un peu long, on peut remplacer par
    # DEMI_CASE = TAILLE_CASE // 2
    # # p.ex. enumerate(['a', 'b', 'c']) = [(0, 'a'), ('1', 'b'), (2, 'c')
    # for (rangee, rangee_de_commandes) in enumerate(
    #         [['no', 'n', 'ne'],
    #          ['o', 'Zzz', 'e'],
    #          ['so', 's', 'se']]):
    #     for (colonne, commande) in enumerate(rangee_de_commandes):
    #         # `+ DEMI_CASE' pour se décaler au milieu de la case, afin de
    #         # centrer `anchor=center' le texte au milieu de la case
    #         canvas.create_text(colonne * TAILLE_CASE + DEMI_CASE,
    #                            rangee * TAILLE_CASE + DEMI_CASE,
    #                            text=commande, anchor='center')
    canvas.create_text(0 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       0 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='no', anchor='center')
    canvas.create_text(1 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       0 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='n', anchor='center')
    canvas.create_text(2 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       0 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='ne', anchor='center')
    canvas.create_text(0 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       1 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='o', anchor='center')
    canvas.create_text(1 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       1 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='Zzz', anchor='center')
    canvas.create_text(2 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       1 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='e', anchor='center')
    canvas.create_text(0 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       2 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='so', anchor='center')
    canvas.create_text(1 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       2 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='s', anchor='center')
    canvas.create_text(2 * TAILLE_CASE + TAILLE_CASE // 2, # distance horizontale
                       2 * TAILLE_CASE + TAILLE_CASE // 2, # distance verticale
                       text='se', anchor='center')
    # dessiner le terrain en parcourant toutes les cases rangée par rangée ...
    for rangee in range(rangees(terrain_de_jeu)):
        # ... puis dans la rangée, parcourons chaque colonne
        for colonne in range(colonnes(terrain_de_jeu)):
            # `+ 4' pour laisser la place aux commandes sur la gauche du terrain
            x_origine = (colonne + 4) * TAILLE_CASE
            y_origine = rangee * TAILLE_CASE
            # Choisir l'affichage en fonction du contenu de la case
            if case(terrain_de_jeu, rangee, colonne) == OBSTACLE:
                montre_obstacle(canvas, x_origine, y_origine)
            elif case(terrain_de_jeu, rangee, colonne) == JOUEUR:
                montre_joueur(canvas, x_origine, y_origine)
            elif case(terrain_de_jeu, rangee, colonne) == ROBOT:
                montre_robot(canvas, x_origine, y_origine)

def joueur(terrain_de_jeu):
    "Donne la position (rangée, colonne) du joueur sur le terrain"
    # p.ex. next(i for i in [1, 3, 2] if i > 1), parcourt la liste [1, 3, 2],
    # donnant tour à tour la valeur 1, 3, puis 2 à i.  Dès que i > 1 (donc 3),
    # arrêter de chercher et prendre 3 comme solution.
    return next(((rangee, colonne)
                 for rangee in range(rangees(terrain_de_jeu))
                 for colonne in range(colonnes(terrain_de_jeu))
                 if case(terrain_de_jeu, rangee, colonne) == JOUEUR))

def approche(coordonnee_robot, coordonnee_joueur):
    """Calcule une nouvelle coordonnée pour le robot afin de s'approcher du joueur

    Cette fonction est utilisée séparèment pour la rangée et pour la colonne."""
    if coordonnee_robot < coordonnee_joueur:
        # Si le robot et plus {à gauche/haut} que le joueur, aller {à droite/plus bas}
        return coordonnee_robot + 1
    elif coordonnee_robot > coordonnee_joueur:
        # Si le robot et plus {à droite/bas} que le joueur, aller {à gauche/plus haut}
        return coordonnee_robot - 1
    else:
        # Si le robot est à la même distance du {bord gauche/haut}, que le
        # joueur, ne rien changer dans cette direction
        return coordonnee_robot

def bouge_robots(terrain_de_jeu):
    # D'abord calculer la position du joueur puisque tous les robots veulent s'en rapprocher
    (rangee_joueur, colonne_joueur) = joueur(terrain_de_jeu)
    # Pour ne pas changer le terrain de jeu avant d'avoir bougé tous les
    # robots, nous calculons d'abord toutes les nouvelles positions des
    # robots (stockées dans cette liste):
    nouvelles_positions = []
    # Parcourons tout le tableau, rangée par rangée ...
    for rangee in range(rangees(terrain_de_jeu)):
        # ... et colonne par colonne pour trouver tous les robots
        for colonne in range(colonnes(terrain_de_jeu)):
            if case(terrain_de_jeu, rangee, colonne) == ROBOT:
                # Puisque nous avons trouvé un robot, calculons la nouvelle
                # position ...
                nouvelle_rangee = approche(rangee, rangee_joueur)
                nouvelle_colonne = approche(colonne, colonne_joueur)
                # ... et mettons la de côté
                nouvelles_positions.append((nouvelle_rangee, nouvelle_colonne))
                # nous retirons le robot temporairement, nous le remettrons
                # en place grâce à nouvelles_positions.
                terrain_de_jeu[rangee][colonne] = VIDE
    # Remettre les robots en place en tenant compte des collisions
    for (rangee, colonne) in nouvelles_positions:
        if (rangee == rangee_joueur) and (colonne == colonne_joueur):
            # un robot a rattrapé le joueur
            return False
        # si on arrive ici: la case est soit VIDE, ROBOT ou OBSTACLE:
        assert case(terrain_de_jeu, rangee, colonne) in [VIDE, ROBOT, OBSTACLE]
        if case(terrain_de_jeu, rangee, colonne) != VIDE:
            # collision -> la case devient inaccessible
            terrain_de_jeu[rangee][colonne] = OBSTACLE
        else:
            # il y a place pour le robot: on le remet à sa place
            terrain_de_jeu[rangee][colonne] = ROBOT
    # Si on arrive ici, aucun robot n'a rattrapé le joueur, le jeu peut continuer
    return True

PASSER_SON_TOUR = (0, 0) # le joueur ne veut pas bouger
# Les 8 directions dans lesquelles peut bouger le joueur
NORD = (-1, 0) # -1: vers le haut, 0: ni à gauche, ni à droite
NORD_EST = (-1, 1) # -1: vers le haut, 1: vers la droite
EST = (0, 1) # ... etc ...
SUD_EST = (1, 1)
SUD = (1, 0)
SUD_OUEST = (1, -1)
OUEST = (0, -1)
NORD_OUEST = (-1, -1)

def bouge_joueur(terrain_de_jeu, direction):
    """Bouge le joueur dans une direction

    Vrai (True) si le joueur a effectué son tour
    Faux (False) si le mouvement était illégal (donc le joueur doit proposer
        un autre mouvement ou demander à passer son tour)"""
    if direction == PASSER_SON_TOUR:
        return True # ne rien faire est toujours possible
    ancienne_rangee, ancienne_colonne = joueur(terrain_de_jeu)
    nouvelle_rangee = ancienne_rangee + direction[0]
    nouvelle_colonne = ancienne_colonne + direction[1]
    if case(terrain_de_jeu, nouvelle_rangee, nouvelle_colonne) == VIDE:
        # il y a de la place, donc nous pouvons effectuer le mouvement
        terrain_de_jeu[ancienne_rangee][ancienne_colonne] = VIDE
        terrain_de_jeu[nouvelle_rangee][nouvelle_colonne] = JOUEUR
        return True # pour signaler le succès du mouvement
    else:
        return False # pour signaler que le mouvement était impossible

def joue(terrain_de_jeu, tk, canvas):
    """Joue une partie sur le terrain de jeu donné

    Vrai (True): le joueur a gagné: tous les robots sont morts avant de l'attraper
    Faux (False): le joueur a perdu"""
    tours = 0 # le nombre de tours auquel le joueur a déjà survécu
    montre_le_terrain(terrain_de_jeu, canvas)
    def action_joueur(evenement):
        "Fonction à appeler pour chaque click souris"
        colonne_click = evenement.x // TAILLE_CASE
        rangee_click = evenement.y // TAILLE_CASE
        if (colonne_click < 0) or (3 <= colonne_click) or (rangee_click < 0) or (3 <= rangee_click):
            # L'utilisateur a cliqué en dehors des commandes, il n'y a rien à
            # faire pour le moment.
            return
        # Si nous arrivons ici, l'utilisateur a cliqué à l'intérieur des
        # commandes, déterminons laquelle:
        direction = [[NORD_OUEST, NORD,            NORD_EST],
                     [OUEST,      PASSER_SON_TOUR, EST],
                     [SUD_OUEST,  SUD,             SUD_EST]
        ][rangee_click][colonne_click]
        if bouge_joueur(terrain_de_jeu, direction):
            # si nous arrivons ici, le mouvement demandé par le joueur est
            # valable:
            nonlocal tours # déclaration nécessaire pour accéder à la variable définie plus haut dans joue()
            tours += 1
            # le joueur a bougé, c'est le tour des robots
            if not bouge_robots(terrain_de_jeu):
                tk.destroy() # ferme la fenêtre et arrête le jeu
                print('Un robot vous a tué après {} tour{}!'.format (
                    tours, '' if tours == 1 else 's'))
            else:
                if robots(terrain_de_jeu) <= 0:
                    # il n'y a plus de robots -> le jeu est fini
                    tk.destroy() # ferme la fenêtre et arrête le jeu
                    print('Félicitations, vous avez survécu à tous les robots')
                else:
                    # le joueur n'est pas encore mort mais il y a encore des
                    # robots, redessinons le terrain
                    montre_le_terrain(terrain_de_jeu, canvas)
    ##### Fin de la définition locale de `action_joueur' ##########
    # PplK 191-193: chaque fois que l'utilisateur cliquera dans le canevas, la
    # fonction action_joueur doit être appelée:
    canvas.bind('<Button-1>', action_joueur)

def partie():
    "Crée un nouveau terrain de jeu puis laisse l'utilisateur jouer avec"
    terrain_de_jeu = nouveau_jeu()
    # Créer une nouvelle fenêtre
    tk = Tk()
    # Et dedans, créer une `toile de peintre' sur laquelle nous pourrons
    # dessiner (PplK 172-)
    canvas = Canvas(tk,
                    # une hauteur suffisante pour le terrain de jeu
                    height=rangees(terrain_de_jeu) * TAILLE_CASE,
                    # une largeur suffisante pour boutons pour diriger le
                    # joueur et le terrain de jeu:
                    width=(4 + colonnes(terrain_de_jeu)) * TAILLE_CASE);
    canvas.pack()
    joue(terrain_de_jeu, tk, canvas)
    tk.mainloop()
