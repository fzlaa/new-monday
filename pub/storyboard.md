# Nouveau Lundi · La pub vidéo

Copie du dossier de travail (version du 19 octobre 2026). Original modifiable : https://claude.ai/code/artifact/51054885-bad1-4166-a6e6-fb2c732d74a5

## Le concept : « Le café chaud »

Un même lundi matin, filmé deux fois, avec un seul personnage : Camille. Avant, son café refroidit pendant qu'elle se noie dans ses tâches. Après une formation Nouveau Lundi, elle le boit encore chaud.

- **Objet fil rouge** : une tasse abricot (`#FE9979`), froide dans la première partie, fumante dans la seconde. Elle fait écho au bandeau du site, « Plus de cafés chauds ».
- **Ton** : chaleureux, malicieux, rassurant. Pas de jargon. L'humour vise la vie de bureau, jamais l'utilisateur.
- **À éviter** : robots, cerveaux, circuits, lueurs bleues, écrans futuristes, marques réelles, texte généré dans l'image (tous les textes s'ajoutent au montage).

## Direction artistique

| Rôle | Couleur | Hex |
| --- | --- | --- |
| Fond, murs, carton final | Crème | `#FDFAF3` |
| Texte, pull de Camille | Vert encre | `#0F241D` |
| Tasse, soleil | Abricot | `#FE9979` |
| Lumière chaude, haut du dégradé du soleil | Abricot clair | `#FFC282` |
| Bulle menthe | Menthe | `#ACE7CC` |
| Bulle pêche | Pêche | `#FDD4C6` |
| Accent doux | Beurre | `#FBEFC2` |

- **Lumière** : lundi d'avant = néon blanc, plat, un peu désaturé (mais clair). Lundi d'après = soleil bas du matin, doré, ombres douces.
- **Décor unique** : le bureau de Camille dans un open space lumineux, grande fenêtre sur les toits, bois clair, plantes.
- **Casting** : Camille, 42 ans, responsable RH, cheveux châtains mi-longs ondulés, lunettes fines dorées, pull vert encre sur chemisier crème. Seule à l'écran.
- **Typo des textes** : Young Serif (titres, bulles) et Albert Sans (mentions), les polices du site. Bulles : coins arrondis 44 px, un coin pointu, fond pêche ou menthe, inclinées de 1 à 2°.
- **Musique** : piano / pizzicati hésitants (lundi d'avant), puis même mélodie enjouée (lundi d'après), environ 100 à 118 BPM. Instrumentale.

## Le script (option A, version courte : 46 s)

**Pas de voix off** (décision de la propriétaire, 19 octobre 2026) : les phrases de la colonne « Voix off » s'affichent à l'écran (Young Serif, vert encre sur crème ou en bulle), la musique seule porte la bande-son.

| # | Temps | Durée générée | Image | Voix off | Texte à l'écran |
| --- | --- | --- | --- | --- | --- |
| 1 | 0:00 – 0:08 | 8 s | Lundi d'avant, plan moyen au bureau. Camille pose sa tasse, regarde son écran, se fige, soupire. | « Lundi, 9 heures. Quarante-sept mails. Une page blanche. » | « Lundi d'avant » |
| 2 | 0:08 – 0:13 | 5 s | Gros plan : elle boit, le café est froid, petite grimace. | « Et un café froid. Encore. » | — |
| 3 | 0:13 – 0:18 | 5 s | Bureau vide face à la fenêtre : le soleil abricot se lève, la lumière dorée envahit le bureau. | « Une formation Nouveau Lundi plus tard… » | « Lundi d'après » en fin de plan |
| 4 | 0:18 – 0:26 | 8 s | Même cadrage que le plan 1, lumière dorée. Tasse fumante, elle tape avec assurance, s'adosse en souriant. | — | Bulle pêche : « Le compte-rendu ? Déjà envoyé. » · Vous, lundi, 9h12 |
| 5 | 0:26 – 0:32 | 6 s | Camille en visio avec un casque, écran flou. Elle hoche la tête et répond avec le sourire. | « Maintenant, c'est vous qu'on vient voir. » | Bulle menthe : « Je vous fais une synthèse d'ici midi. » · Vous, lundi, 10h05 |
| 6 | 0:32 – 0:38 | 6 s | Gros plan, même cadrage que le plan 2 : café chaud, vapeur dans le contre-jour, elle sourit à la caméra. | « Nouveau Lundi. L'IA générative, sans jargon, pour les fonctions support. » | — |
| 7 | 0:38 – 0:46 | montage | Carton final : fond crème, soleil abricot qui se lève derrière « Nouveau Lundi ». | « À lundi ? » | « Nouveau Lundi » puis « À lundi ? » · nouveaulundi.fr |

**Version longue (option A, environ 60 s)** : ajouter 2 ou 3 plans de Camille seule, par exemple la page blanche, Camille qui ferme son ordinateur à 18 h pile, un clin d'œil à la caméra dans le lundi d'après.

**Option B (sans achat, sous 50 crédits, environ 40 s)** : 4 plans générés de 5 s (plans 1, 2, 4, 6) ; le lever de soleil, l'ouverture « Lundi, 9h00 » et le carton final sont des cartons animés faits au montage.

## Prompts

Chaque prompt d'image avec Camille commence par la phrase de continuité et se termine par le bloc de style, la lumière de l'acte et le négatif.

```
Continuité : Keep exactly the same woman from the reference image: same face, same shoulder-length light brown wavy hair, same thin gold-rimmed glasses, same deep green knit sweater over a cream blouse. Only one woman in the frame.
Style : warm modern French corporate office, bright and airy, cream walls (#FDFAF3), light oak wood, green plants, soft apricot (#FE9979) and mint (#ACE7CC) accents, natural skin tones, shot on 35mm lens, shallow depth of field, gentle film grain, cinematic yet realistic, uplifting commercial look. No text, no logos, no robots, no holograms, no glowing blue tech.
Lumière avant : flat cool fluorescent office light, slightly desaturated, overcast window, a bit tired but still bright and clean.
Lumière après : low golden morning sun through large windows, warm apricot glow, soft long shadows, luminous and optimistic.
Négatif : robot, glowing brain, hologram, logo, brand name, readable text on screen, watermark, distorted hands, extra fingers, distorted face, duplicate person.
```

**Fiche personnage**

```
Character reference sheet, photorealistic: Camille, a 42-year-old French woman, HR manager in a large company. Shoulder-length light brown wavy hair, thin gold-rimmed glasses, warm hazel eyes, friendly expressive face, natural minimal makeup. Wears a deep green knit sweater (#0F241D) over a cream blouse. Three views side by side: front, three-quarter, profile. Neutral cream background, soft even light.
```

### Plan 1 · Le bureau, lundi d'avant (8 s, caméra fixe, très léger travelling avant)

```
Image: Medium shot of Camille (reference) sitting at her desk in a bright open-space office on a Monday morning, a large window with city rooftops behind her, an apricot-colored ceramic mug next to her laptop, laptop seen from the side, screen not readable. Lighting: flat cool fluorescent office light, slightly desaturated.
Video: Camille sets the apricot mug down, looks at her laptop screen and freezes in comic disbelief, then exhales slowly and slumps a little in her chair. Static camera with a very slow push-in. Cold desaturated look, quiet office ambience, cinematic, natural motion, her face stays consistent.
```

### Plan 2 · Le café froid (5 s, gros plan fixe)

```
Image: Close-up of Camille at her desk holding the apricot mug near her lips, no steam at all, large window softly out of focus behind her. Lighting: flat cool fluorescent office light, slightly desaturated.
Video: Camille takes a sip, freezes, makes a small disappointed grimace because the coffee is cold, looks down into the mug and slowly puts it away. Static camera. Gentle comedy, expressive but not exaggerated, natural motion, her face stays consistent.
```

### Plan 3 · Le soleil se lève (5 s, caméra fixe, image de départ et de fin)

```
Image de départ: Camille's empty desk in front of the large window, the apricot mug and the closed laptop in the foreground, city rooftops outside at dawn, pale cool light. Same office as shot 1.
Image de fin: Exact same framing, a large round apricot sun risen above the rooftops, warm golden light flooding the desk, the mug and the walls, long soft shadows.
Video: The sun rises above the rooftops, warm apricot light sweeps slowly across the office, the desk and the mug, shadows stretch and soften. Static camera. Magical but realistic, like a time-lapse.
```

### Plan 4 · Le bureau, lundi d'après (8 s, même mouvement que le plan 1)

```
Image: Exact same framing as shot 1 (use the shot 1 image as reference), now bathed in low golden morning sun through the window. Camille, relaxed and smiling, places a steaming apricot mug next to her laptop.
Video: Camille sets down the steaming mug, types confidently and quickly, then leans back in her chair with a satisfied smile. Slow subtle dolly in, same movement as shot 1. Warm, light, optimistic, natural motion, her face stays consistent.
```

### Plan 5 · La visio (6 s, caméra fixe)

```
Image: Over-the-shoulder medium shot of Camille at her desk wearing a light headset during a video call, the laptop screen softly blurred with colored blocks, steaming apricot mug, golden morning light from the window.
Video: Camille listens on her headset, nods calmly, then answers with a confident smile and an open hand gesture, perfectly at ease. Static camera. Warm morning light, calm office ambience, cinematic, natural motion, her face stays consistent.
```

### Plan 6 · Le café chaud (6 s, très lent travelling avant)

```
Image: Exact same framing as shot 2 (use the shot 2 image as reference), golden backlight from the window. Camille holds the apricot mug with both hands, generous steam rising, eyes half closed, peaceful smile.
Video: Camille takes a sip of hot coffee, steam curling in the golden light, she closes her eyes with pleasure, then opens them and looks straight into the camera with a warm, slightly mischievous smile. Very slow push in, natural motion, her face stays consistent.
```

### Plan 7 · Carton final (montage, pas de génération)

Fond crème `#FDFAF3`, « Nouveau Lundi » en Young Serif vert encre `#0F241D`, soleil abricot (dégradé `#FFC282` → `#FE9979`) qui monte derrière le « i » de Lundi, comme en haut du site. Puis « À lundi ? » et nouveaulundi.fr.
