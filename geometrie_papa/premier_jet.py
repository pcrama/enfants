# https://cocalc.com
# %matplotlib inline
# import math
# from matplotlib import pyplot as plt
# from matplotlib import image

import math
import numpy as np
from matplotlib import pyplot as plt

BLANC_TRANSPARENT = [1.0, 1.0, 1.0, 0.0]

def image_vide(_x, _y):
    "Une image transparente"
    return BLANC_TRANSPARENT

def superpose(*images):
    "Superpose plusieurs images (la première image est au-dessus)"
    if images == []:
        return image_vide
    images = list(images) # une copie pour être sûr que personne ne la modifie
    def moyenne_ponderee(xs, idx, somme):
        return sum(v[idx] * v[3] for v in xs) / somme
    def images_superposees(x, y):
        valeurs = []
        for img in images:
            valeurs.append(img(x, y))
            if valeurs[-1][3] > 0.9999:
                # l'image est tellement opaque qu'on ne regarde pas derrière
                break
        somme_opacite = sum(v[3] for v in valeurs)
        if somme_opacite < 1e-6:
            return BLANC_TRANSPARENT
        else:
            return [moyenne_ponderee(valeurs, 0, somme_opacite)
                   , moyenne_ponderee(valeurs, 1, somme_opacite)
                   , moyenne_ponderee(valeurs, 2, somme_opacite)
                   , max(v[3] for v in valeurs)]
    return images_superposees

def longueur_au_carre(v):
    "Calcule le carré de la longueur d'un vecteur"
    return sum(x * x for x in v)

def longueur_du_vecteur(v):
    "Calcule la longueur d'un vecteur"
    return math.sqrt(longueur_au_carre(v))

def produit_scalaire(w1, w2):
    "Calcule le produit scalaire de deux vecteurs"
    return sum(x * y for (x, y) in zip(w1, w2))

def pavage_parallelogramme(image, coin_1, coin_2, coin_3):
    """Répète infiniment un parallélogramme (défini par 3 coins) découpé dans l'image
    c3 .
        \
         +________.x
          \        \
           \        \
            \        \
             .________+____.
            c1             c2"""
    #  _     ___     ___
    #  x = a c   + b c
    #         21      32
    #                                                       ___
    #  / x     x   \ / a \   / v \  NB: x  = x component of c
    #  |  21    31 | |   |   |   |       21                  21
    #  |           | |   | = |   |      a and b are the unknowns
    #  | y     y   | | b |   | w |                         _   __
    #  \  21    31 / \   /   \   /      v = x component of x - c
    #                                                           1
    # By matrix inversion, we get
    # / a \                     / y     -x   \ / v \
    # |   |           1         |  31     31 | |   |
    # |   | = ----------------- |            | |   |
    # | b |    x  y   - y  x    | -y    x    | | w |
    # \   /     21 31    21 31  \   21   21  / \   /
    x21, y21 = v1 = [x2 - x1 for (x1, x2) in zip(coin_1, coin_2)]
    x31, y31 = v2 = [x3 - x1 for (x1, x3) in zip(coin_1, coin_3)]
    det = x21 * y31 - x31 * y21
    if abs(det) < 1e-6:
        # les vecteurs sont (presque) colinéaires
        return image_vide
    def image_pavee(x, y):
        v, w = [x - coin_1[0], y - coin_1[1]]
        a = (v * y31 - w * x31) / det
        b = (-v * y21 + w * x21) / det
        vx = a % 1.0
        vy = b % 1.0
        return image(coin_1[0] + vx * v1[0] + vy * v2[0],
                     coin_1[1] + vx * v1[1] + vy * v2[1])
    return image_pavee

def translation(image, v):
    "Effectue une translation d'une image: l'origine est envoyée sur le point v"
    dx, dy = v
    def apres_translation(x, y):
        return image(x - dx, y - dy)
    return apres_translation

def rotation(image, angle_degres, cx=0, cy=0):
    "Effectue un rotation d'une image autour du centre ((0, 0) par défaut)"
    c = math.cos(math.pi * angle_degres / 180)
    s = math.sin(math.pi * angle_degres / 180)
    # (1, 0) dans la nouvelle image est (c, -s) dans l'ancienne image
    # (0, 1) dans la nouvelle image est (s, c) dans l'ancienne image
    def image_tournee(x, y):
        dx = x - cx
        dy = y - cy
        return image(cx + c * dx + s * dy, cy - s * dx + c * dy)
    return image_tournee

def decoupe_rectangulaire(image, coin_1, coin_2, couleur_autour=BLANC_TRANSPARENT):
    "Masque toute l'image autour du rectangle et remplace l'extérieur par une couleur constante"
    bbox = [[min(coin_1[0], coin_2[0]), min(coin_1[1], coin_2[1])],
            [max(coin_1[0], coin_2[0]), max(coin_1[1], coin_2[1])]]
    def image_tronquee(x, y):
        if (bbox[0][0] <= x <= bbox[1][0]) and (bbox[0][1] <= y <= bbox[1][1]):
            return image(x, y)
        else:
            return couleur_autour
    return image_tronquee

def decoupe_circulaire(image, centre, rayon, couleur_autour=BLANC_TRANSPARENT):
    "Masque toute l'image autour du cercle et remplace l'extérieur par une couleur constante"
    rayon_carre = rayon * rayon
    def image_tronquee(x, y):
        dx = x - centre[0]
        dy = y - centre[1]
        if (dx * dx + dy * dy) <= rayon_carre:
            return image(x, y)
        else:
            return couleur_autour
    return image_tronquee

def projette(image, coin_1, coin_2, pixels_par_unite):
    "Rend l'image visible, limité au rectangle défini par les coins et à la résolution donnée"
    bbox = [[min(coin_1[0], coin_2[0]), min(coin_1[1], coin_2[1])],
            [max(coin_1[0], coin_2[0]), max(coin_1[1], coin_2[1])]]
    w = bbox[1][0] - bbox[0][0]
    h = bbox[1][1] - bbox[0][1]
    pw = round(w * pixels_par_unite)
    ph = round(h * pixels_par_unite)
    data = np.ones((ph, pw, 4), dtype=np.double)
    for py in range(0, ph):
        # 0     1     2     3     4     5    (ph = 6, pixels_par_unite=2)
        # 1.25  0.75  0.25  -0.25 -0.75 -1.25 (h = 3, min = -1.5, max = 1.5)
        y = bbox[1][1] - 1 / (2.0 * pixels_par_unite) - py / pixels_par_unite
        for px in range(0, pw):
            x = bbox[0][0] + px / pixels_par_unite + 1 / (2.0 * pixels_par_unite)
            data[py, px, :] = image(x, y)
    return data

def montre(image, coin_1, coin_2, pixels_par_unite):
    "Affiche la partie l'image limité au rectangle défini par les coins"
    plt.imshow(projette(image, coin_1, coin_2, pixels_par_unite))

def opaque(image, opacite=1.0):
    "Rend l'image opaque (vois aussi superpose)"
    def opacifie(x, y):
        p = image(x, y)
        return [p[0], p[1], p[2], opacite]
    return opacifie

def ligne(point_1, point_2, epaisseur, rgba):
    "Dessine un ligne passant par les 2 points donnés"
    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]
    longueur = math.sqrt(dx * dx + dy * dy)
    dx /= longueur
    dy /= longueur
    demi_epaisseur = epaisseur / 2.0
    def image_ligne(x, y):
        a = x - point_1[0]
        b = y - point_1[1]
        if abs(-a * dy + b * dx) <= demi_epaisseur:
            return rgba
        else:
            return BLANC_TRANSPARENT
    return image_ligne

def cercle(centre, rayon, epaisseur, rgba):
    "Dessine un cercle"
    rayon_2_minimum = (rayon - epaisseur / 2) * (rayon - epaisseur / 2)
    rayon_2_maximum = (rayon + epaisseur / 2) * (rayon + epaisseur / 2)
    def image_cercle(x, y):
        dx = x - centre[0]
        dy = y - centre[1]
        if rayon_2_minimum <= dx * dx + dy * dy <= rayon_2_maximum:
            return rgba
        else:
            return BLANC_TRANSPARENT
    return image_cercle

def disque(centre, rayon, rgba):
    "Dessine un cercle rempli"
    rayon_2 = rayon * rayon
    def image_disque(x, y):
        dx = x - centre[0]
        dy = y - centre[1]
        if dx * dx + dy * dy <= rayon_2:
            return rgba
        else:
            return BLANC_TRANSPARENT
    return image_disque

def homothetie(image, centre, facteur):
    "Déforme l'image par homothétie"
    # (ax, ay) est transforme en (cx + (ax - cx) * f, cy + (ay - cy) * f)
    # donc
    # x = cx + (ax - cx) * f <=> ax = cx + (x - cx) / f
    def image_agrandie(x, y):
        return image(centre[0] + (x - centre[0]) / facteur,
                     centre[1] + (y - centre[1]) / facteur)
    return image_agrandie

def segment(point_1, point_2, epaisseur, rgba):
    "Dessine un segment de droite reliant deux points"
    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]
    longueur_carre = dx * dx + dy * dy
    longueur = math.sqrt(longueur_carre)
    dx /= longueur
    dy /= longueur
    demi_epaisseur = epaisseur / 2.0
    def image_ligne(x, y):
        a = x - point_1[0]
        b = y - point_1[1]
        if abs(-a * dy + b * dx) <= demi_epaisseur:
            # nous sommes dans la ligne, mais sommes-nous aussi dans le segment?
            if 0 <= a * dx + b * dy <= longueur:
                return rgba
            else:
                return BLANC_TRANSPARENT
        else:
            return BLANC_TRANSPARENT
    return image_ligne

def multi_segments(segments, epaisseur, rgba):
    "Plus efficace que superpose(segment(...), segment(...), ...)"
    def image(x, y):
        for s in segments:
            v = s(x, y)
            if v == rgba:
                return v
        return BLANC_TRANSPARENT
    return image

def polygone(coins, epaisseur, rgba):
    "Dessine un polygone reliant les coins"
    cotes = zip(coins, [coins[-1], *coins[:-1]])
    segments = [segment(c[0], c[1], epaisseur, rgba) for c in cotes]
    return multi_segments(segments, epaisseur, rgba)

def polygone_regulier(centre, rayon, cotes, epaisseur, rgba):
    points = [[centre[0] + rayon * math.cos(2 * math.pi / cotes * i),
               centre[1] + rayon * math.sin(2 * math.pi / cotes * i)]
              for i in range(cotes)]
    return polygone(points, epaisseur, rgba)

def im1(x, y):
    return [max(0, min(1, (x + 1) / 1.5)), 0, 0, 0.99]

def im2(x, y):
    return [0, max(0, min(1, (x + 1) / 2)), 0, 0.99]

if __name__ == "__main__":
    montre(superpose(ligne([0.1, -0.3], [0.5, -0.3], 0.5, [1.0, 0.0, 0.0, 1.0]),
                     ligne([0.1, 3.3], [0.5, -0.3], 0.5, [0.0, 1.0, 0.0, 1.0]),
                     segment([0.1, 0.3], [-0.5, 0.3], 0.25, [1.0, 0.0, 0.0, 0.5]),
                     segment([0.2, 0.2], [-0.6, 0.4], 0.25, [0.0, 1.0, 0.0, 0.5]),
                     segment([0.3, 0.3], [-0.6, 0.5], 0.25, [0.0, 0.0, 1.0, 0.5])),
           [-1, -1],
           [1, 1],
           32)
