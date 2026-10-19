"""Montage de la pub « Léa » aux couleurs du site (58 s, 1280×720, 25 i/s).

Reprend le déroulé et la musique de la pub de référence (pub/reference-pub-lea.md),
avec les textes, les bulles et le carton de fin dans le style de pub/montage.py.

Usage : python3 pub/montage_lea.py DOSSIER_TRAVAIL SORTIE.mp4
  DOSSIER_TRAVAIL contient fonts/ (comme pour montage.py), plans/plan1.mp4 à
  plans/plan8.mp4 (plans fournis par la propriétaire) et musique.wav (piste
  audio de la pub de référence).
"""
import os
import subprocess
import sys
from functools import lru_cache

from PIL import Image, ImageDraw

import montage as m
from montage import (BEURRE, CREME, ENCRE, FINE, FPS, H, MENTHE, PECHE, SANS, SANS_GRAS, SERIF, W,
                     apparition, avec_bulle, avec_pastille, clamp, couper_lignes, ease_in_out, ease_out, largeur,
                     ombre, poser, rect_arrondi, texte_seul, texte_suivi)

TRAVAIL, SORTIE = sys.argv[1], sys.argv[2]
DUREE = 58.0
soleil = lru_cache(None)(m.soleil)


# ---------- éléments ----------

@lru_cache(None)
def legende(etiquette, texte):
    """Carton crème en bas à gauche : petite étiquette (soleil + heure) puis la phrase."""
    f = SERIF(40)
    lignes = couper_lignes(texte, f, 760, -0.02)
    lh = 49
    fe = SANS_GRAS(19)
    haut_e = 34 if etiquette else 0
    w = int(max([largeur(l, f, -0.02) for l in lignes] + [fe.getlength(etiquette) + 30])) + 2 * 32
    h = haut_e + lh * len(lignes) + 2 * 20
    c = rect_arrondi(w, h, (26, 26, 26, 6), CREME)
    d = ImageDraw.Draw(c)
    if etiquette:
        c.alpha_composite(soleil(9), (32, 24))
        d.text((32 + 26, 20), etiquette, font=fe, fill=ENCRE + (190,))
    for i, l in enumerate(lignes):
        texte_suivi(d, (32, 16 + haut_e + i * lh), l, f, ENCRE)
    return ombre(c, 16, (0, 10), 0.3)


def avec_legende(img, lt, etiquette, texte, debut, fin):
    a, dy = apparition(lt, debut, fin)
    poser(img, legende(etiquette, texte), 64 - 40, H - 56 + dy + 40, a, ancre=(0, 1))


@lru_cache(None)
def images_plan(n):
    dossier = os.path.join(TRAVAIL, "images", f"plan{n}")
    if not os.path.isdir(dossier):
        os.makedirs(dossier)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", os.path.join(TRAVAIL, "plans", f"plan{n}.mp4"), "-vf",
             f"fps={FPS},scale={W}:{H}:flags=lanczos", "-q:v", "2", os.path.join(dossier, "%04d.jpg")],
            check=True)
    return sorted(os.path.join(dossier, f) for f in os.listdir(dossier))


def plan(n, lt):
    imgs = images_plan(n)
    return Image.open(imgs[int(clamp(lt * FPS, 0, len(imgs) - 1))]).convert("RGBA")


# ---------- séquences ----------

AVANT, APRES = ("Lundi dernier", BEURRE), ("Nouveau lundi", MENTHE)


def p1(lt, d):
    img = plan(1, lt)
    avec_pastille(img, lt, *AVANT)
    avec_legende(img, lt, "Lundi dernier · 8 h 57", "312 mails non lus.", 0.9, d - 0.15)
    return img


def p2(lt, d):
    img = plan(2, lt)
    avec_pastille(img, lt, *AVANT, 0.0)
    avec_legende(img, lt, "10 h 30", "Des notes que personne ne relira.\nVous non plus.", 0.7, d - 0.15)
    return img


def p3(lt, d):
    img = plan(3, lt)
    avec_pastille(img, lt, *AVANT, 0.0, d - 0.3)
    avec_legende(img, lt, "18 h 30", "Vous partez tard, avec l’impression d’avoir couru toute la journée.",
                 0.6, d - 0.5)
    return img


def p4(lt, d):
    img = plan(4, lt)
    avec_legende(img, lt, "", f"Et si lundi devenait votre jour préféré{FINE}?", 1.6, d - 0.15)
    return img


def p5(lt, d):
    img = plan(5, lt)
    avec_pastille(img, lt, *APRES, 0.4)
    avec_legende(img, lt, "Nouveau lundi · 8 h 57", "312 mails. 5 priorités.\nAvant la fin du café.", 1.0, d - 0.15)
    return img


def p6(lt, d):
    img = plan(6, lt)
    avec_pastille(img, lt, *APRES, 0.0)
    avec_bulle(img, lt, f"«{FINE}Le compte rendu\nest déjà parti.{FINE}»", "Vous, lundi, 10 h 45", PECHE, "gauche",
               1.5, 0.7, d - 0.15, 70, H - 70)
    return img


def p7(lt, d):
    img = plan(7, lt)
    avec_pastille(img, lt, "La formation", PECHE, 0.0)
    avec_legende(img, lt, "La formation Nouveau Lundi",
                 "On ne vous apprend pas l’IA.\nOn vous apprend votre travail, avec l’IA.", 0.5, d - 0.15)
    return img


def p8(lt, d):
    img = plan(8, lt)
    avec_pastille(img, lt, *APRES, 0.0, d - 0.3)
    avec_legende(img, lt, "18 h 30", "Vous partez à l’heure.\nVos collègues se posent des questions.", 0.5, d - 0.5)
    return img


def fin(lt, d):
    """Carton final : le grand soleil de la pub de référence et la signature du site."""
    img = Image.new("RGBA", (W, H), CREME + (255,))
    # grand soleil abricot qui monte du bas
    R = 470
    k = ease_out((lt - 0.1) / 2.2)
    poser(img, soleil(R), W / 2, H + R - 40 - 300 * k, 1.0, ancre=(0.5, 0.5))
    # « Nouveau Lundi », avec le petit soleil derrière « di » comme en haut du site
    taille = 92
    titre = texte_seul("Nouveau Lundi", taille, suivi=-0.035)
    a = ease_out((lt - 0.5) / 0.7)
    y0 = 58 + int(20 * (1 - a))
    tx = W / 2 - titre.width / 2
    r = int(0.46 * taille)
    sx = tx + titre.width - 10 + 0.3 * taille - r
    sy = y0 + SERIF(taille).getbbox("L")[1] + 0.12 * taille
    poser(img, soleil(r), sx, sy + 0.8 * taille * (1 - ease_out((lt - 0.7) / 1.4)), clamp((lt - 0.7) / 0.3),
          ancre=(0.5, 0.5))
    poser(img, titre, W / 2, y0, a, ancre=(0.5, 0))
    a2, dy2 = apparition(lt, 1.2, 99, 0.5)
    poser(img, texte_seul("Lundi prochain ne ressemblera pas au précédent.", 38), W / 2, 188 + dy2, a2,
          ancre=(0.5, 0))
    a3, dy3 = apparition(lt, 1.6, 99, 0.5)
    poser(img, texte_seul("Formation à l’IA générative · Garanti sans robot.", 22, ENCRE, serif=False, suivi=0),
          W / 2, 246 + dy3, a3 * 0.8, ancre=(0.5, 0))
    # sur le soleil : « À lundi ? » et l'adresse
    a4, dy4 = apparition(lt, 2.8, 99, 0.5)
    poser(img, texte_seul(f"À lundi{FINE}?", 70), W / 2, 445 + dy4, a4, ancre=(0.5, 0))
    a5, dy5 = apparition(lt, 3.3, 99, 0.5)
    poser(img, texte_seul("nouveaulundi.fr", 28, serif=False, suivi=0), W / 2, 548 + dy5, a5, ancre=(0.5, 0))
    return img


SEQUENCES = [(p1, 7.0), (p2, 6.0), (p3, 5.0), (p4, 7.0), (p5, 8.0), (p6, 7.0), (p7, 5.5), (p8, 6.5), (fin, 6.0)]
FONDUS = {2: 1.2, 7: 0.8}  # fondu après la séquence i (durée en s) ; coupes franches ailleurs
assert abs(sum(d for _, d in SEQUENCES) - DUREE) < 1e-6
DEBUTS = [sum(d for _, d in SEQUENCES[:i]) for i in range(len(SEQUENCES))]


def image(t):
    i = max(j for j, s in enumerate(DEBUTS) if s <= t + 1e-9)
    f, d = SEQUENCES[i]
    img = f(t - DEBUTS[i], d)
    for j, fd in FONDUS.items():
        bord = DEBUTS[j + 1]
        if abs(t - bord) < fd / 2:
            k = (t - (bord - fd / 2)) / fd  # 0 → séquence j, 1 → séquence j + 1
            a = SEQUENCES[j][0](t - DEBUTS[j], SEQUENCES[j][1])
            b = SEQUENCES[j + 1][0](t - DEBUTS[j + 1], SEQUENCES[j + 1][1])
            img = Image.blend(a, b, ease_in_out(k))
    return img.convert("RGB")


if __name__ == "__main__":
    seul = os.environ.get("IMAGE")
    if seul:
        image(float(seul)).save(SORTIE)
        sys.exit()
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", os.path.join(TRAVAIL, "musique.wav"),
         "-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", "-t", str(DUREE), SORTIE],
        stdin=subprocess.PIPE)
    for n in range(int(DUREE * FPS)):
        enc.stdin.write(image(n / FPS).tobytes())
        if n % 250 == 0:
            print(f"{n / FPS:.0f} s", flush=True)
    enc.stdin.close()
    sys.exit(enc.wait())
