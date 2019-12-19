# https://cocalc.com
# %matplotlib inline
import math
import numpy as np
from matplotlib import pyplot as plt

def image_vide(_x, _y):
    return BLANC_TRANSPARENT

def superpose(*images):
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
    return sum(x * x for x in v)

def longueur_du_vecteur(v):
    return math.sqrt(longueur_au_carre(v))

def produit_scalaire(w1, w2):
    return sum(x * y for (x, y) in zip(w1, w2))

def pavage_parallelogramme(image, coin_1, coin_2, coin_3):
    v1 = [x2 - x1 for (x1, x2) in zip(coin_1, coin_2)]
    v2 = [x3 - x1 for (x1, x3) in zip(coin_1, coin_3)]
    if abs(v2[0] * v1[1] - v2[1] * v1[0]) < 1e-6:
        # les vecteurs sont (presque) collineaires
        return image_vide
    l1 = longueur_du_vecteur(v1)
    l2 = longueur_du_vecteur(v2)
    v1 = [x / l1 for x in v1]
    v2 = [x / l2 for x in v2]
    def image_pavee(x, y):
        xy = [x - coin_1[0], y - coin_1[1]]
        vx = produit_scalaire(xy, v1) % l1
        vy = produit_scalaire(xy, v2) % l2
        return image(coin_1[0] + vx * v1[0] + vy * v2[0],
                     coin_1[1] + vx * v1[1] + vy * v2[1])
    return image_pavee

def translation(image, dx, dy):
    def apres_translation(x, y):
        return image(x - dx, y - dy)
    return apres_translation

def rotation(image, angle):
    c = math.cos(math.pi * angle / 180)
    s = math.sin(math.pi * angle / 180)
    # (1, 0) dans la nouvelle image est (c, -s) dans l'ancienne image
    # (0, 1) dans la nouvelle image est (s, c) dans l'ancienne image
    def image_tournee(x, y):
        return image(c * x + s * y, -s * x + c * y)
    return image_tournee

def decoupe_rectangulaire(image, coin_1, coin_2):
    bbox = [[min(coin_1[0], coin_2[0]), min(coin_1[1], coin_2[1])],
            [max(coin_1[0], coin_2[0]), max(coin_1[1], coin_2[1])]]
    def image_tronquee(x, y):
        if (bbox[0][0] <= x <= bbox[1][0]) and (bbox[0][1] <= y <= bbox[1][1]):
            return image(x, y)
        else:
            return BLANC_TRANSPARENT
    return image_tronquee

def decoupe_circulaire(image, centre, rayon):
    rayon_carre = rayon * rayon
    def image_tronquee(x, y):
        dx = x - centre[0]
        dy = y - centre[1]
        if (dx * dx + dy * dy) <= rayon_carre:
            return image(x, y)
        else:
            return BLANC_TRANSPARENT
    return image_tronquee

def projette(image, coin_1, coin_2, pixels_par_unite):
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

def opaque(image):
    def opacifie(x, y):
        p = image(x, y)
        return [p[0], p[1], p[2], 1.0]
    return opacifie

BLANC_TRANSPARENT = [1.0, 1.0, 1.0, 0.0]

def ligne(point_1, point_2, epaisseur, rgba):
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
    # (ax, ay) est transforme en (cx + (ax - cx) * f, cy + (ay - cy) * f)
    # donc
    # x = cx + (ax - cx) * f <=> ax = cx + (x - cx) / f
    def image_agrandie(x, y):
        return image(centre[0] + (x - centre[0]) / facteur,
                     centre[1] + (y - centre[1]) / facteur)
    return image_agrandie

def segment(point_1, point_2, epaisseur, rgba):
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

def polygone(coins, epaisseur, rgba):
    cotes = zip(coins, [coins[-1], *coins[:-1]])
    segments = [segment(c[0], c[1], epaisseur, rgba) for c in cotes]
    def image(x, y):
        for s in segments:
            v = s(x, y)
            if v == rgba:
                return v
        return BLANC_TRANSPARENT
    return image

def im1(x, y):
    return [max(0, min(1, (x + 1) / 1.5)), 0, 0, 0.99]

def im2(x, y):
    return [0, max(0, min(1, (x + 1) / 2)), 0, 0.99]

plt.imshow(projette(superpose(ligne([0.1, -0.3], [0.5, -0.3], 0.5, [1.0, 0.0, 0.0, 1.0]),
                              ligne([0.1, 3.3], [0.5, -0.3], 0.5, [0.0, 1.0, 0.0, 1.0]),
                              segment([0.1, 0.3], [-0.5, 0.3], 0.25, [1.0, 0.0, 0.0, 0.5]),
                              segment([0.2, 0.2], [-0.6, 0.4], 0.25, [0.0, 1.0, 0.0, 0.5]),
                              segment([0.3, 0.3], [-0.6, 0.5], 0.25, [0.0, 0.0, 1.0, 0.5])),
                    [-1, -1],
                    [1, 1],
                    32))
# plt.imshow(projette(superpose(superpose(translation(ligne([0.1, , 0.0, -0.5), im1),
#                               superpose(translation(im2, 0.0, 0.5), im2)),
#                     [-1, -1],
#                     [1, 1],
#                     256),
#            interpolation='nearest')
