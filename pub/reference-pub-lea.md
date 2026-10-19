# Pub de référence « Léa » (vidéo fournie le 19 octobre 2026)

La propriétaire veut **la même pub, aux couleurs du site**. Fichier analysé : `pub-finale-1.mp4`, 58 s, 1280×720, 30 i/s, AAC stéréo. Le storyboard d'origine, adapté aux couleurs du site, a été envoyé à la propriétaire.

## Déroulé observé

| Temps | Plan | Image | Texte à l'écran (étiquette · phrase) |
| --- | --- | --- | --- |
| 0:00 – 0:07 | 1 | Léa à son bureau, ciel de pluie, gobelet en carton ; elle se fige, puis rabat l'écran à moitié | « Lundi dernier · 8h57 » · « 312 mails non lus. » |
| 0:07 – 0:13 | 2 | Réunion dans une salle grise, un collègue bâille, horloge, Léa prend des notes | « 10h30 » · « Des notes que personne ne relira. Vous non plus. » |
| 0:13 – 0:18 | 3 | Bureau vide la nuit, une lampe ; Léa enfile son manteau, épuisée | « 18h30 » · « Vous partez tard. Avec l'impression d'avoir couru toute la journée. » |
| 0:18 – 0:25 | 4 | Fondu vers la fenêtre : un grand demi-soleil se lève sur la ville, lumière dorée, bureau vide | « Et si lundi devenait votre jour préféré ? » (sans étiquette) |
| 0:25 – 0:33 | 5 | Même Léa, lumière du matin, tasse fumante, ordinateur, sourire | « Nouveau lundi · 8h57 » · « 312 mails. 5 priorités. Avant la fin du café. » |
| 0:33 – 0:40 | 6 | Fin de réunion dans une salle lumineuse et pleine de plantes ; on rit, un collègue lève le pouce | « 10h45 » · « Le compte rendu est déjà parti. » |
| 0:40 – 0:45,5 | 7 | Atelier de formation : grande table en bois, ordinateurs, formateur qui aide, rires | « La formation » · « On ne vous apprend pas l'IA. On vous apprend votre travail, avec l'IA. » |
| 0:45,5 – 0:52 | 8 | Léa part à l'heure, sac à l'épaule, fait coucou ; deux collègues intrigués, horloge | « 18h30 » · « Vous partez à l'heure. Vos collègues se posent des questions. » |
| 0:52 – 0:58 | Carton | Fond beige, grand demi-soleil jaune → orange qui monte du bas | Logo demi-soleil + « nouveau lundi », « Lundi prochain ne ressemblera pas au précédent. », « Formation à l'IA générative · Garanti sans robot. » |

## Style observé

- **Personnage** : Léa, la quarantaine, cheveux auburn courts et bouclés, lunettes rondes foncées, cardigan moutarde sur une chemise blanche. Seul personnage récurrent, avec des figurants (réunion, atelier, collègues).
- **Lundi dernier** (plans 1 à 3) : tons froids, gris-bleu, désaturés, pluie puis nuit.
- **Nouveau lundi** (plans 5 à 8) : lumière dorée, chaude, plantes, bois clair, orange.
- **Légendes** : en bas à gauche, cadre arrondi (environ 16 px), petite icône demi-soleil abricot + étiquette en petit (heure ou « La formation »), puis la phrase en gros, police large type Syne. Sur les plans froids : fond bleu nuit, étiquette jaune, texte blanc. Sur les plans chauds : fond crème, texte bleu nuit. Apparition en fondu au début de chaque plan.
- **Transitions** : coupes franches, fondu lent vers le lever de soleil, fondu vers le carton final.
- **Son** : musique seule, sans voix off. Calme et clairsemée de 0 à 18 s, pleine et enjouée à partir du lever de soleil (18 s), dernier accord sous le carton (52 s), puis fin.

## Adaptation aux couleurs du site (à appliquer)

- Bleu nuit des légendes froides → **vert encre `#0F241D`**, étiquettes en **beurre `#FBEFC2`**, texte en **crème `#FDFAF3`**.
- Légendes chaudes : fond **crème `#FDFAF3`**, texte **vert encre**. Quelques phrases en **bulles pêche `#FDD4C6` ou menthe `#ACE7CC`** (coins de 44 px, un coin pointu), comme sur le site.
- Polices : **Young Serif** (phrases, titre) et **Albert Sans** (étiquettes) au lieu de Syne.
- Icône et soleil : disque **abricot clair `#FFC282` → abricot `#FE9979`**, comme en haut du site, au lieu du demi-soleil jaune.
- Carton final : fond **crème `#FDFAF3`**, « Nouveau Lundi » en Young Serif vert encre, avec le soleil qui se lève derrière « Lundi ».
- Images générées : cardigan de Léa en **vert encre**, tasse en céramique **abricot**, accents abricot, beurre et menthe dans les plans chauds.

## Coût et contrainte

8 plans animés pour environ 52 s : avec Wan 3.0 en 720p (1,75 crédit par seconde sur le compte, remise de 60 % jusqu'au 31 octobre 2026), cela fait environ 91 crédits, plus environ 10 crédits d'images, soit **environ 100 crédits**. Le solde est de 7,76 crédits (offre gratuite) : il faut l'offre **Starter** (270 crédits), que seule la propriétaire peut acheter.

## Montage livré (19 octobre 2026)

`video/pub.mp4` (58 s, 12 Mo, sur le site depuis le 19 octobre 2026 au soir ; d'abord livrée sous le nom `pub-lea.mp4`), fait avec `pub/montage_lea.py` à partir des 8 plans fournis par la propriétaire (`plan1.mp4` à `plan8.mp4`, non versionnés car lourds) et de la musique de la pub de référence. Aucun crédit Higgsfield dépensé. Textes dans le style de la pub de 50 s (« pub DA ») : cartons crème et texte vert encre en Young Serif, étiquettes beurre (« Lundi dernier »), menthe (« Nouveau lundi ») et pêche (« La formation »), bulle pêche au plan 6. Carton de fin : mélange des deux fins, avec le grand soleil abricot qui monte du bas (référence) et la signature « Nouveau Lundi » avec son petit soleil, puis « À lundi ? » et nouveaulundi.fr (pub DA), sur fond crème. La pub de Camille (50 s) est conservée sous `video/pub-camille.mp4`.
