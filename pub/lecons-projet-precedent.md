# Leçons d'un projet Higgsfield précédent

Résumé du journal de génération d'un autre projet de pub (personnage « Léa », 8 plans, 58 s), partagé le 19 octobre 2026.

## Ce qui a marché

- **Wan 3.0 Prime, 720p, 16:9, en image vers vidéo** : 8 plans de 6 à 8 s, tous réussis au premier essai.
- **Images de départ avec un modèle d'édition d'image** (`alibaba/qwen-image-3/edit`, 1k, 16:9, environ 0,64 crédit API) et le portrait du personnage en référence : le visage reste le même d'un plan à l'autre.
- **Soul v2** (`higgsfield-ai/soul/v2/standard`) pour le portrait de référence et les plans sans personnage : 4 variantes pour 0,20 crédit API.
- **Phrase de continuité identique** en tête de chaque prompt d'image (visage, coiffure, lunettes, vêtement) et un **négatif commun** : `robot, glowing brain, logo, brand name, readable text on screen, watermark, distorted hands, extra fingers, distorted faces`.
- **Prompts vidéo** qui finissent par `cinematic, natural motion, her face stays consistent` et décrivent l'ambiance sonore.
- **Écran d'ordinateur** décrit comme `blurred screen with colored blocks` plutôt que du texte.
- **Musique** : Lyria (API Gemini), environ 0,08 $ pour une piste de 60 s. Style retenu : pizzicati paresseux, tuba, piano désaccordé à 72 BPM, puis même mélodie enjouée à 118 BPM avec glockenspiel et célesta, accord final.
- **Poster** tiré d'une image d'un plan, **image de partage** montée à partir du fond du carton final : aucun crédit en plus.

## Erreurs à éviter

- Personnage **apparu deux fois** dans une image de groupe : préciser « only one woman in the frame ».
- **Travelling latéral** : la caméra a quitté le personnage après 3 s. Rester en caméra fixe ou léger travelling avant.
- **Action précise sur un objet** non réalisée (une lampe qui ne s'éteint pas) : ne faire dépendre aucun texte ni aucune réplique d'un geste précis.
- **Variantes non téléchargées** à cause d'une erreur de script : télécharger chaque résultat tout de suite.
- **Modèle momentanément indisponible** : échec non facturé, relancer plus tard.

## Coûts observés (crédits API, 1 crédit = 0,0625 $)

| Poste | Crédits |
| --- | --- |
| Images de test (12 images) | 5,72 |
| Plans vidéo (8 plans, 56 s, Wan 3.0 Prime 720p avec son) | 50,18 |
| Visuels du site (4 images) | 1,35 |
| Total | 58,75 (environ 3,70 $) |

Pour comparaison, sur le compte Higgsfield de l'application (crédits différents), le 19 octobre 2026 : Wan 3.0 Prime 720p 7 s = 21 crédits, Wan 3.0 720p = 1,75 crédit par seconde, Wan 3.0 1080p = 3,5 crédits par seconde, image `gpt_image_2_5` = 0,25 crédit, `nano_banana_2` = 1,5 crédit, voix off `seed_audio` (texte complet) = 1,7 crédit.
