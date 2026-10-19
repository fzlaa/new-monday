"""Musique originale de la pub Nouveau Lundi (50 s), composée en code.

Lundi d'avant (0-18 s) : pizzicati et piano hésitants, 80 BPM.
Lever du soleil (18-23 s) : nappe qui monte et arpège de célesta.
Lundi d'après (23-41 s) : même mélodie, enjouée, 120 BPM, glockenspiel, basse, shaker.
Carton final (41-50 s) : accord final, puis petite question « À lundi ? ».

Usage : python3 pub/musique.py sortie.wav
"""
import sys
import wave

import numpy as np

SR = 48000
DUREE = 50.0
rng = np.random.default_rng(7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def env(n, attaque, chute):
    t = np.arange(n) / SR
    e = np.exp(-t / chute)
    a = int(attaque * SR)
    if a > 0:
        e[:a] *= np.linspace(0, 1, a)
    return e


def pizz(midi, dur=0.6):
    """Corde pincée (Karplus-Strong)."""
    f = hz(midi)
    n = int(dur * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * env(n, 0.002, dur / 3)


def piano(midi, dur=1.2, desaccord=0.0):
    f = hz(midi) * (1 + desaccord)
    n = int((dur + 0.6) * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k, a in enumerate([1, 0.5, 0.28, 0.14, 0.08], start=1):
        s += a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.2 + 0.9 * k))
    s += 0.3 * np.sin(2 * np.pi * f * 1.003 * t) * np.exp(-t * 1.5)
    rel = np.ones(n)
    r = int(dur * SR)
    rel[r:] = np.linspace(1, 0, n - r)
    return s * rel * env(n, 0.004, 9)


def glock(midi, dur=1.0):
    f = hz(midi)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
    return s * env(n, 0.001, 0.45)


def celesta(midi, dur=0.9):
    f = hz(midi)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 8)
    return s * env(n, 0.002, 0.35)


def basse(midi, dur=0.45):
    f = hz(midi)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    return s * env(n, 0.005, dur / 2.5)


def shaker(dur=0.08):
    n = int(dur * SR)
    s = rng.uniform(-1, 1, n)
    s = np.diff(s, prepend=0)
    return s * env(n, 0.01, dur / 3)


def nappe(midis, dur, montee=True):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in midis:
        f = hz(m)
        for det in (-0.004, 0, 0.004):
            s += np.sin(2 * np.pi * f * (1 + det) * t + rng.uniform(0, 6.28))
            s += 0.3 * np.sin(4 * np.pi * f * (1 + det) * t)
    s /= len(midis) * 3
    forme = (t / dur) ** 1.5 if montee else np.ones(n)
    forme = forme * np.minimum(1, (dur - t) / 0.3)
    return s * forme


class Piste:
    def __init__(self):
        self.g = np.zeros((int(DUREE * SR) + SR * 3, 2))

    def pose(self, son, debut, vol=1.0, pan=0.0):
        i = int(debut * SR)
        son = son * vol
        gauche, droite = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
        self.g[i:i + len(son), 0] += son * gauche
        self.g[i:i + len(son), 1] += son * droite


# Mélodie commune (4 mesures en 4/4, temps en noires) : do majeur, C | Am | F | G
MELODIE = [
    (64, 0, 1), (67, 1, 1), (69, 2, 1.5), (67, 3.5, 0.5),
    (64, 4, 1), (62, 5, 1), (60, 6, 2),
    (65, 8, 1), (69, 9, 1), (72, 10, 1.5), (71, 11.5, 0.5),
    (67, 12, 1), (69, 13, 0.5), (71, 13.5, 0.5), (67, 14, 2),
]
ACCORDS = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])]

p = Piste()

# --- Lundi d'avant : 80 BPM, 6 mesures, 0 à 18 s ---
noire = 60 / 80
for mes in range(6):
    racine, acc = ACCORDS[mes % 4]
    t0 = mes * 4 * noire
    p.pose(pizz(racine - 12 + 12, 0.7), t0, 0.55, -0.3)
    p.pose(pizz(racine + 7, 0.6), t0 + 2 * noire, 0.4, -0.3)
    for k, m in enumerate(acc):
        p.pose(pizz(m, 0.5), t0 + (1 + 2 * (k % 2)) * noire + 0.02 * k, 0.18, 0.35)
for m, debut, dur in MELODIE + [(n, d + 16, l) for n, d, l in MELODIE[:7]]:
    # piano hésitant : un peu en retard, légèrement désaccordé, quelques notes lâchées
    if debut in (13.5, 3.5):
        continue
    retard = rng.uniform(0.03, 0.12) + (0.18 if debut in (2, 9, 18) else 0)
    p.pose(piano(m, dur * noire * 0.9, desaccord=0.004), debut * noire + retard, 0.32, 0.1)

# --- Lever du soleil : 18 à 23 s ---
p.pose(nappe([55, 59, 62, 65], 5.0), 18.0, 1.1)
for i, m in enumerate([67, 71, 74, 77, 79, 83, 86]):
    p.pose(celesta(m, 1.2), 19.6 + i * 0.42, 0.4, -0.5 + i * 0.15)

# --- Lundi d'après : 120 BPM, 9 mesures, 23 à 41 s ---
noire = 0.5
T = 23.0
for mes in range(9):
    racine, acc = ACCORDS[mes % 4] if mes < 8 else (43, [55, 59, 62])
    t0 = T + mes * 2.0
    for b in range(4):
        p.pose(basse(racine - 12 if b % 2 == 0 else racine - 5, 0.4), t0 + b * noire, 0.35)
        p.pose(shaker(), t0 + b * noire + 0.25, 0.06, 0.4)
        p.pose(shaker(0.05), t0 + b * noire, 0.035, 0.4)
    for b in (1, 3):
        for m in acc:
            p.pose(piano(m, 0.25), t0 + b * noire, 0.11, -0.2)
    for i, m in enumerate(acc + [acc[1]]):
        p.pose(pizz(m + 12, 0.3), t0 + i * noire + 0.25, 0.12, 0.45)
for m, debut, dur in MELODIE + [(n, d + 16, l) for n, d, l in MELODIE[:7]]:
    t = T + debut * noire
    if t >= 41:
        continue
    p.pose(piano(m + 12, dur * noire * 0.85), t, 0.28, 0.05)
    p.pose(glock(m + 12, 0.8), t, 0.14, -0.25)
# petite montée vers l'accord final
for i, m in enumerate([67, 69, 71, 72]):
    p.pose(glock(m + 12, 0.5), 40.0 + i * 0.25, 0.16)

# --- Carton final : 41 à 50 s ---
for m in [36, 48, 55, 60, 64, 67, 72, 76]:
    p.pose(piano(m, 3.5), 41.0, 0.24)
p.pose(nappe([48, 55, 60, 64, 67], 6.5, montee=False) * np.linspace(1, 0, int(6.5 * SR)), 41.0, 0.7)
p.pose(glock(84, 1.5), 41.0, 0.15)
# « À lundi ? » : deux notes qui montent, sans résoudre
p.pose(piano(67, 0.6), 45.6, 0.45)
p.pose(glock(79, 1.0), 45.6, 0.2)
p.pose(piano(74, 1.6), 46.2, 0.45)
p.pose(glock(86, 1.5), 46.2, 0.2)
p.pose(pizz(43, 1.2), 46.2, 0.3)

# --- mixage : petite réverbération, limitation douce ---
g = p.g[: int(DUREE * SR)]
rev = np.zeros_like(g)
for retard, gain in [(0.031, 0.35), (0.047, 0.3), (0.071, 0.25), (0.113, 0.2), (0.167, 0.15)]:
    d = int(retard * SR)
    rev[d:] += g[:-d] * gain
    rev[d:, ::-1] += g[:-d] * gain * 0.3
g = g + 0.35 * rev
fin = int(1.5 * SR)
g[-fin:] *= np.linspace(1, 0, fin)[:, None]
g = np.tanh(g / np.max(np.abs(g)) * 1.4) / np.tanh(1.4) * 0.9

with wave.open(sys.argv[1] if len(sys.argv) > 1 else "musique.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((g * 32767).astype(np.int16).tobytes())
