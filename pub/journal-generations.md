# Journal des générations · pub Nouveau Lundi

Option B validée par la propriétaire le 19 octobre 2026 : 50 s au total, 4 plans animés, le reste en plans fixes et cartons animés, **sans voix off**. Budget : les 50 crédits du compte (offre gratuite).

Limites de l'offre gratuite constatées : une seule génération à la fois ; `gpt_image_2_5` et `nano_banana` refusés (« Requires basic plan or higher ») ; `soul_2`, `seedream_v5_lite` et `wan3_0` acceptés.

Les fichiers sont dans `pub/rendus/`.

| # | Plan | Modèle | Prompt (résumé) | Coût | Résultat | Gardé |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Portrait de Camille | `soul_2` 2k, 3:4 | Portrait, 42 ans, cheveux châtains ondulés, lunettes dorées, pull vert, fond crème | 0,12 | `00-portrait-camille.jpg`, très bon | Oui (référence) |
| 2 | Plan 4, image de départ | `soul_2` 2k + portrait en référence | Bureau, lumière dorée | 0,12 | La référence est prise comme style : nouveau portrait, pas de bureau | Non (raté, non conservé) |
| 3 | Plan 1, image de départ | `seedream_v5_lite` + portrait | Plan moyen au bureau, néon froid, tasse abricot, ordinateur de profil | 1 | `01-avant-bureau.jpg`, même visage, décor réussi | Oui |
| 4 | Plan 1, vidéo 5 s | `wan3_0` 720p 16:9, sans son | Elle se fige devant l'écran, soupire et s'affaisse ; caméra fixe, léger travelling avant | 8,75 | `p1-avant-bureau.mp4`, réussi au premier essai (30 i/s) | Oui |
| 5 | Plan 2, image de départ | `seedream_v5_lite` + portrait + image du plan 1 | Gros plan, tasse abricot aux lèvres, pas de vapeur, néon froid | 1 | `02-avant-cafe-froid.jpg`, très bon | Oui |
| 6 | Plan 2, vidéo 5 s | `wan3_0` 720p 16:9, sans son | Elle boit, grimace (café froid), baisse la tasse ; caméra fixe | 8,75 | `p2-avant-cafe-froid.mp4`, grimace réussie au premier essai | Oui |
| 7 | Plan 4, image de départ | `seedream_v5_lite` + image du plan 1 + portrait | Même cadrage, soleil doré, sourire, tasse fumante | 1 | `04-apres-bureau-v2.jpg`, très bon | Oui |
| 8 | Plan 4, vidéo 5 s | `wan3_0` 720p 16:9, sans son | Elle tape avec assurance, s'adosse en souriant, vapeur ; léger travelling avant | 8,75 | `p4-apres-bureau.mp4`, réussi au premier essai (vapeur un peu généreuse) | Oui |
| 9 | Plan 6, image de départ | `seedream_v5_lite` + image du plan 2 + image du plan 4 | Même cadrage que le plan 2, contre-jour doré, tasse à deux mains, vapeur, yeux mi-clos | 1 | `06-apres-cafe-chaud.jpg`, très bon | Oui |
| 10 | Plan 6, vidéo 5 s | `wan3_0` 720p 16:9, sans son | Elle boit le café chaud, ferme les yeux, puis regarde la caméra en souriant ; très lent travelling avant | 8,75 | `p6-apres-cafe-chaud.mp4`, réussi au premier essai | Oui |
| 11 | Plan fixe « mails » | `seedream_v5_lite` + image du plan 1 | Par-dessus l'épaule : boîte mail floue pleine, page blanche, tasse froide, papiers | 1 | `f1-avant-mails.jpg`, très bon | Oui |
| 12 | Plan fixe « visio » | `seedream_v5_lite` + image du plan 4 + portrait | Casque, sourire, main ouverte, écran flou, tasse fumante, lumière dorée | 1 | `f2-apres-visio.jpg`, très bon | Oui |
| 13 | Plan fixe « 18 h » | `seedream_v5_lite` + image du plan 4 + portrait | Fin d'après-midi dorée, elle ferme l'ordinateur, manteau sur le bras, sac | 1 | `f3-apres-18h.jpg`, très bon | Oui |

**Total dépensé : 42,24 crédits** sur 50 (solde restant : environ 7,76). Aucune seconde prise n'a été nécessaire.

Hors Higgsfield, sans crédit : musique composée en code (`pub/musique.py`), montage, cartons et bulles en code (`pub/montage.py`).
