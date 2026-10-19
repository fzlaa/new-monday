"""Montage de la pub Nouveau Lundi (50 s, 1280×720, 25 i/s).

Compose image par image les plans animés, les plans fixes (léger zoom),
les cartons, les textes et les bulles, puis encode avec la musique.

Usage : python3 pub/montage.py DOSSIER_TRAVAIL SORTIE.mp4
  DOSSIER_TRAVAIL doit contenir fonts/ (YoungSerif.ttf, AlbertSans-Medium.ttf,
  AlbertSans-Bold.ttf) et musique.wav (python3 pub/musique.py).
Les rendus Higgsfield sont lus dans pub/rendus/.
"""
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUREE = 1280, 720, 25, 50.0
TRAVAIL, SORTIE = sys.argv[1], sys.argv[2]
RENDUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rendus")
SS = 3  # suréchantillonnage des formes

CREME = (253, 250, 243)
ENCRE = (15, 36, 29)
ABRICOT = (254, 153, 121)
ABRICOT_CLAIR = (255, 194, 130)
MENTHE = (172, 231, 204)
PECHE = (253, 212, 198)
BEURRE = (251, 239, 194)
GRIS_FROID = (236, 239, 238)


def police(nom, taille):
    return ImageFont.truetype(os.path.join(TRAVAIL, "fonts", nom), taille)


SERIF = lambda t: police("YoungSerif.ttf", t)
SANS = lambda t: police("AlbertSans-Medium.ttf", t)
SANS_GRAS = lambda t: police("AlbertSans-Bold.ttf", t)


# ---------- courbes ----------

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 3 * x * x - 2 * x * x * x


def ressort(x):
    """Arrivée avec un léger dépassement (comme --spring sur le site)."""
    x = clamp(x)
    return 1 - math.exp(-6 * x) * math.cos(9 * x)


# ---------- dessin ----------

FINE = "\u202f"  # espace fine insécable, avant ? ! : et dans les guillemets


def avance(c, font):
    return 0.6 * font.getlength(" ") if c == FINE else font.getlength(c)


def largeur(texte, font, suivi):
    return sum(avance(c, font) for c in texte) + suivi * font.size * (len(texte) - 1)


def texte_suivi(draw, xy, texte, font, fill, suivi=-0.02):
    x, y = xy
    for c in texte:
        if c != FINE:
            draw.text((x, y), c, font=font, fill=fill)
        x += avance(c, font) + suivi * font.size


def rect_arrondi(w, h, rayons, couleur):
    """Rectangle aux coins arrondis (haut-gauche, haut-droit, bas-droit, bas-gauche)."""
    im = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w * SS, h * SS], fill=255)
    coins = [(0, 0), (w * SS, 0), (w * SS, h * SS), (0, h * SS)]
    for (cx, cy), r in zip(coins, rayons):
        r *= SS
        if r <= 0:
            continue
        sx = 1 if cx == 0 else -1
        sy = 1 if cy == 0 else -1
        x0, y0 = (cx, cy) if sx > 0 else (cx - r, cy)
        y0 = cy if sy > 0 else cy - r
        d.rectangle([x0, y0, x0 + r, y0 + r], fill=0)
        ox, oy = cx + sx * r, cy + sy * r
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=255)
    masque = im.resize((w, h), Image.LANCZOS)
    calque = Image.new("RGBA", (w, h), couleur + (255,))
    calque.putalpha(masque)
    return calque


def ombre(calque, flou=18, decalage=(0, 14), opacite=0.28):
    m = 40
    w, h = calque.size
    out = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    a = calque.getchannel("A").point(lambda v: int(v * opacite))
    sh = Image.new("RGBA", calque.size, (15, 36, 29, 0))
    sh.putalpha(a)
    out.alpha_composite(sh, (m + decalage[0], m + decalage[1]))
    out = out.filter(ImageFilter.GaussianBlur(flou))
    out.alpha_composite(calque, (m, m))
    return out


def soleil(rayon):
    """Disque abricot en dégradé radial, comme .hero__sun."""
    taille = 2 * rayon * SS
    yy, xx = np.mgrid[0:taille, 0:taille] / taille
    d = np.sqrt((xx - 0.45) ** 2 + (yy - 0.35) ** 2) / 0.7
    t = np.clip(d, 0, 1)[..., None]
    rgb = np.array(ABRICOT_CLAIR) * (1 - t) + np.array(ABRICOT) * t
    im = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
    m = Image.new("L", (taille, taille), 0)
    ImageDraw.Draw(m).ellipse([0, 0, taille - 1, taille - 1], fill=255)
    im.putalpha(m)
    return im.resize((2 * rayon, 2 * rayon), Image.LANCZOS)


def couper_lignes(texte, font, max_l, suivi):
    """Coupe aux « \n » imposés, puis quand la ligne dépasse max_l."""
    lignes = []
    for para in texte.split("\n"):
        cour = ""
        for m in filter(None, para.split(" ")):
            essai = (cour + " " + m).strip()
            if largeur(essai, font, suivi) > max_l and cour:
                lignes.append(cour)
                cour = m
            else:
                cour = essai
        lignes.append(cour)
    return lignes


# ---------- éléments graphiques (rendus une fois) ----------

@lru_cache(None)
def legende(texte):
    """Carton crème en bas à gauche : remplace la voix off."""
    f = SERIF(44)
    lignes = couper_lignes(texte, f, 820, -0.02)
    lh = 54
    w = int(max(largeur(l, f, -0.02) for l in lignes)) + 2 * 34
    h = lh * len(lignes) + 2 * 24
    c = rect_arrondi(w, h, (28, 28, 28, 6), CREME)
    d = ImageDraw.Draw(c)
    for i, l in enumerate(lignes):
        texte_suivi(d, (34, 18 + i * lh), l, f, ENCRE)
    return ombre(c, 16, (0, 10), 0.3)


@lru_cache(None)
def bulle(texte, sous_titre, couleur, cote, inclinaison):
    f = SERIF(42)
    lignes = couper_lignes(texte, f, 620, -0.02)
    lh = 50
    w = int(max(largeur(l, f, -0.02) for l in lignes)) + 2 * 40
    h = lh * len(lignes) + 2 * 30
    rayons = (44, 44, 44, 8) if cote == "gauche" else (44, 44, 8, 44)
    b = rect_arrondi(w, h, rayons, couleur)
    d = ImageDraw.Draw(b)
    for i, l in enumerate(lignes):
        texte_suivi(d, (40, 22 + i * lh), l, f, ENCRE)
    b = ombre(b, 20, (0, 16), 0.25)
    fs = SANS(23)
    lw = int(fs.getlength(sous_titre)) + 40
    lab = rect_arrondi(lw, 42, (21, 21, 21, 21), CREME)
    ImageDraw.Draw(lab).text((20, 8), sous_titre, font=fs, fill=ENCRE + (210,))
    out = Image.new("RGBA", (max(b.width, lw + 100), b.height + 40), (0, 0, 0, 0))
    out.alpha_composite(b, (0, 0))
    lx = 52 if cote == "gauche" else b.width - lw - 52
    out.alpha_composite(lab, (lx, b.height - 30))
    return out.rotate(inclinaison, resample=Image.BICUBIC, expand=True)


@lru_cache(None)
def pastille(texte, couleur, inclinaison=-4):
    f = SANS_GRAS(24)
    w = int(f.getlength(texte)) + 44
    p = rect_arrondi(w, 50, (25, 25, 25, 25), couleur)
    ImageDraw.Draw(p).text((22, 10), texte, font=f, fill=ENCRE)
    p = ombre(p, 12, (0, 8), 0.25)
    return p.rotate(inclinaison, resample=Image.BICUBIC, expand=True)


@lru_cache(None)
def texte_seul(texte, taille, couleur=ENCRE, serif=True, suivi=-0.03):
    f = SERIF(taille) if serif else SANS(taille)
    w = int(largeur(texte, f, suivi)) + 20
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (w, asc + desc + 10), (0, 0, 0, 0))
    texte_suivi(ImageDraw.Draw(im), (10, 0), texte, f, couleur + (255,), suivi)
    return im


def poser(fond, el, x, y, alpha=1.0, echelle=1.0, ancre=(0, 0)):
    """Colle un élément RGBA avec opacité et échelle ; ancre = point fixe (fraction)."""
    if alpha <= 0.01:
        return
    if abs(echelle - 1) > 0.002:
        el = el.resize((max(1, int(el.width * echelle)), max(1, int(el.height * echelle))), Image.BICUBIC)
    if alpha < 0.999:
        el = el.copy()
        el.putalpha(el.getchannel("A").point(lambda v: int(v * alpha)))
    fond.alpha_composite(el, (int(x - ancre[0] * el.width), int(y - ancre[1] * el.height)))


# ---------- sources ----------

@lru_cache(None)
def source_image(nom):
    return Image.open(os.path.join(RENDUS, nom)).convert("RGB")


def plan_fixe(nom, lt, duree, z0=1.0, z1=1.08, cx=(0.5, 0.5), cy=(0.5, 0.5)):
    """Léger zoom (Ken Burns) sur une image haute définition."""
    im = source_image(nom)
    sw, sh = im.size
    k = ease_in_out(lt / duree) * 0.85 + (lt / duree) * 0.15
    z = z0 + (z1 - z0) * k
    base = min(sw / W, sh / H)
    vw, vh = W * base / z, H * base / z
    x = (cx[0] + (cx[1] - cx[0]) * k) * sw - vw / 2
    y = (cy[0] + (cy[1] - cy[0]) * k) * sh - vh / 2
    x, y = clamp(x, 0, sw - vw), clamp(y, 0, sh - vh)
    s = vw / W
    return im.transform((W, H), Image.AFFINE, (s, 0, x, 0, s, y), resample=Image.BICUBIC).convert("RGBA")


@lru_cache(None)
def images_video(nom):
    dossier = os.path.join(TRAVAIL, "images", nom)
    if not os.path.isdir(dossier):
        os.makedirs(dossier)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", os.path.join(RENDUS, nom), "-vf",
             f"fps={FPS},scale={W}:{H}:flags=lanczos", "-q:v", "2", os.path.join(dossier, "%04d.jpg")],
            check=True)
    return sorted(os.path.join(dossier, f) for f in os.listdir(dossier))


def plan_anime(nom, lt, z0=1.0, z1=1.0):
    imgs = images_video(nom)
    i = int(clamp(lt * FPS, 0, len(imgs) - 1))
    im = Image.open(imgs[i]).convert("RGBA")
    if z0 != 1 or z1 != 1:
        z = z0 + (z1 - z0) * clamp(lt / (len(imgs) / FPS))
        w, h = int(W * z), int(H * z)
        im = im.resize((w, h), Image.BICUBIC).crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))
    return im


def fond_uni(couleur):
    return Image.new("RGBA", (W, H), couleur + (255,))


def melange(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


# ---------- animations de texte ----------

def apparition(lt, debut, fin, entree=0.35, sortie=0.25):
    """Opacité et décalage vertical d'un texte affiché entre debut et fin."""
    if lt < debut or lt > fin:
        return 0.0, 0
    a = ease_out((lt - debut) / entree) * clamp((fin - lt) / sortie)
    return a, int(18 * (1 - ease_out((lt - debut) / entree)))


def avec_legende(img, lt, texte, debut, fin):
    a, dy = apparition(lt, debut, fin)
    poser(img, legende(texte), 64 - 40, H - 60 + dy + 40, a, ancre=(0, 1))


def avec_bulle(img, lt, texte, sous_titre, couleur, cote, incl, debut, fin, x, y):
    if lt < debut or lt > fin:
        return
    e = ressort((lt - debut) / 0.55)
    a = clamp((lt - debut) / 0.2) * clamp((fin - lt) / 0.25)
    ancre = (0.05, 1) if cote == "gauche" else (0.95, 1)
    poser(img, bulle(texte, sous_titre, couleur, cote, incl), x, y, a, 0.82 + 0.18 * e, ancre)


def avec_pastille(img, lt, texte, couleur, debut=0.3, fin=99):
    if lt < debut or lt > fin:
        return
    e = ressort((lt - debut) / 0.5)
    poser(img, pastille(texte, couleur), 48, 40, clamp((lt - debut) / 0.15), 0.7 + 0.3 * e)


# ---------- séquences ----------

def ouverture(lt, d):
    """0 à 3,5 s : « Lundi d'avant », lumière froide."""
    img = fond_uni(GRIS_FROID)
    a = ease_out((lt - 0.2) / 0.6)
    titre = texte_seul("Lundi d’avant", 128)
    poser(img, titre, W / 2, H / 2 + 20 + 20 * (1 - a), a, ancre=(0.5, 0.5))
    if lt > 0.9:
        e = ressort((lt - 0.9) / 0.5)
        poser(img, pastille("Lundi, 9 h 00", BEURRE, -6), W / 2 - 250, H / 2 - 120, clamp((lt - 0.9) / 0.15), 0.7 + 0.3 * e, (0.5, 0.5))
    return img


def p1(lt, d):
    img = plan_anime("p1-avant-bureau.mp4", lt)
    avec_pastille(img, lt, "Lundi d’avant", BEURRE)
    avec_legende(img, lt, "Quarante-sept mails.", 1.0, d - 0.3)
    return img


def fixe_mails(lt, d):
    img = plan_fixe("f1-avant-mails.jpg", lt, d, 1.02, 1.14, (0.5, 0.56), (0.5, 0.55))
    avec_pastille(img, lt, "Lundi d’avant", BEURRE, 0.0)
    avec_legende(img, lt, "Une page blanche.", 0.4, d - 0.3)
    return img


def p2(lt, d):
    img = plan_anime("p2-avant-cafe-froid.mp4", lt)
    avec_pastille(img, lt, "Lundi d’avant", BEURRE, 0.0)
    avec_legende(img, lt, "Et un café froid. Encore.", 0.8, d - 0.3)
    return img


def lever(lt, d):
    """18 à 23 s : le soleil se lève, « Lundi d'après »."""
    k = ease_in_out(lt / 3.2)
    img = fond_uni(melange(GRIS_FROID, CREME, k))
    r = 230
    y = H + r + 40 - (r + 330) * ease_out(lt / 3.4)
    poser(img, soleil(r), W / 2, y, 1.0, ancre=(0.5, 0.5))
    a1, dy1 = apparition(lt, 0.3, 2.9, 0.5, 0.35)
    poser(img, texte_seul("Une formation Nouveau Lundi plus tard…", 54), W / 2, 150 + dy1, a1, ancre=(0.5, 0.5))
    a2 = ease_out((lt - 2.9) / 0.5)
    poser(img, texte_seul("Lundi d’après", 128), W / 2, H / 2 - 30 + 20 * (1 - a2), a2, ancre=(0.5, 0.5))
    return img


def p4(lt, d):
    img = plan_anime("p4-apres-bureau.mp4", lt)
    avec_pastille(img, lt, "Lundi d’après", MENTHE, 0.0)
    avec_bulle(img, lt, "«\u202fLe compte-rendu\u202f?\nDéjà envoyé.\u202f»", "Vous, lundi, 9 h 12", PECHE, "gauche", 1.5,
               0.9, d - 0.2, 70, H - 70)
    return img


def fixe_visio(lt, d):
    img = plan_fixe("f2-apres-visio.jpg", lt, d, 1.0, 1.08, (0.5, 0.45), (0.5, 0.45))
    avec_pastille(img, lt, "Lundi d’après", MENTHE, 0.0)
    avec_bulle(img, lt, "«\u202fJe vous fais une\nsynthèse d’ici midi.\u202f»", "Vous, lundi, 10 h 05", MENTHE, "droite", -1.5,
               0.4, 2.6, W - 70, H - 70)
    avec_legende(img, lt, "Maintenant,\nc’est vous qu’on vient voir.", 2.75, d - 0.25)
    return img


def fixe_soir(lt, d):
    img = plan_fixe("f3-apres-18h.jpg", lt, d, 1.0, 1.08, (0.5, 0.54), (0.45, 0.4))
    avec_pastille(img, lt, "Lundi d’après", MENTHE, 0.0)
    avec_legende(img, lt, "18 h. Et on rentre à l’heure.", 0.3, d - 0.25)
    return img


def p6(lt, d):
    img = plan_anime("p6-apres-cafe-chaud.mp4", lt)
    avec_legende(img, lt, "L’IA générative, sans jargon, pour les fonctions support.", 0.6, d - 0.2)
    return img


def final(lt, d):
    """41 à 50 s : soleil derrière « Nouveau Lundi », puis « À lundi ? »."""
    img = fond_uni(CREME)
    taille = 150
    l1, l2 = texte_seul("Nouveau", taille, suivi=-0.035), texte_seul("Lundi", taille, suivi=-0.035)
    a = ease_out((lt - 0.1) / 0.7)
    dy = int(24 * (1 - a))
    haut = 145
    # soleil : se lève derrière le « di » de Lundi, comme en haut du site
    r = int(0.46 * taille)
    lx = W / 2 - l2.width / 2
    sx = lx + l2.width - 10 + 0.3 * taille - r
    sy_fin = haut + 60 + SERIF(taille).getbbox("L")[1] + 0.12 * taille
    k = ease_out((lt - 0.5) / 2.0)
    sy = sy_fin + 1.4 * taille * (1 - k)
    poser(img, soleil(r), sx, sy, clamp((lt - 0.5) / 0.4), ancre=(0.5, 0.5))
    poser(img, l1, W / 2, haut - 0.88 * taille + dy + 60, a, ancre=(0.5, 0))
    poser(img, l2, W / 2, haut + 60 + dy, a, ancre=(0.5, 0))
    a2, dy2 = apparition(lt, 4.6, 99, 0.5)
    poser(img, texte_seul("À lundi\u202f?", 64), W / 2, 500 + dy2, a2, ancre=(0.5, 0))
    a3, dy3 = apparition(lt, 5.3, 99, 0.5)
    poser(img, texte_seul("nouveaulundi.fr", 30, serif=False, suivi=0), W / 2, 596 + dy3, a3, ancre=(0.5, 0))
    return img


SEQUENCES = [  # (fonction, durée)
    (ouverture, 3.5), (p1, 5.0), (fixe_mails, 4.5), (p2, 5.0), (lever, 5.0),
    (p4, 5.0), (fixe_visio, 5.0), (fixe_soir, 3.0), (p6, 5.0), (final, 9.0),
]
FONDU = 0.16
assert abs(sum(d for _, d in SEQUENCES) - DUREE) < 1e-6

debuts = np.cumsum([0] + [d for _, d in SEQUENCES])


def image(t):
    i = int(np.searchsorted(debuts, t, side="right") - 1)
    i = min(i, len(SEQUENCES) - 1)
    f, d = SEQUENCES[i]
    lt = t - debuts[i]
    img = f(lt, d)
    voisin = None
    if lt < FONDU and i > 0:
        voisin, k = i - 1, 0.5 - lt / (2 * FONDU)
    elif d - lt < FONDU and i < len(SEQUENCES) - 1:
        voisin, k = i + 1, 0.5 - (d - lt) / (2 * FONDU)
    if voisin is not None and k > 0.01:
        fv, dv = SEQUENCES[voisin]
        img = Image.blend(img, fv(t - debuts[voisin], dv), k)
    return img.convert("RGB")


if __name__ == "__main__":
    n = int(DUREE * FPS)
    seul = os.environ.get("IMAGE")  # IMAGE=12.3 : exporte une seule image pour vérifier
    if seul:
        image(float(seul)).save(SORTIE)
        sys.exit()
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", os.path.join(TRAVAIL, "musique.wav"),
         "-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", "-shortest", SORTIE],
        stdin=subprocess.PIPE)
    for k in range(n):
        enc.stdin.write(image(k / FPS).tobytes())
        if k % 125 == 0:
            print(f"{k / FPS:.0f} s", flush=True)
    enc.stdin.close()
    sys.exit(enc.wait())
