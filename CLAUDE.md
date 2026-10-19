# Nouveau Lundi

Site vitrine one-page statique (HTML, CSS, JS, sans build) d'un organisme de formation fictif à l'IA générative pour les fonctions support. Hébergé sur GitHub Pages depuis `main`, dossier racine. La propriétaire du projet n'est pas technique : lui répondre en français, simplement, et ne lui demander une action que si personne d'autre ne peut la faire (achat, réglage de compte).

## Structure

- `index.html`, `css/styles.css`, `js/main.js` : le site, fidèle à la maquette « Grand jour » de Claude Design. Mobile sous 760 px (container queries sur `.page`).
- `video/pub.mp4` : la pub (50 s). Le lecteur est une balise `<video>` native (poster, bouton de la maquette, contrôles natifs après le clic) : remplacer le fichier suffit, aucun code à changer.
- `images/` : placeholders (poster de la vidéo, photos, témoignages, image Open Graph). Voir `images/README.md`.
- `pub/storyboard.md` : concept, direction artistique, script et prompts de la pub.
- `pub/lecons-projet-precedent.md` : règles et coûts tirés d'un autre projet Higgsfield. À respecter.
- Chemins relatifs uniquement (le site est servi depuis un sous-dossier). `og:url` et `og:image` pointent vers `https://fzlaa.github.io/new-monday/`.

Palette : crème `#FDFAF3`, vert encre `#0F241D`, abricot `#FE9979`, abricot clair `#FFC282`, menthe `#ACE7CC`, pêche `#FDD4C6`, beurre `#FBEFC2`. Polices : Young Serif et Albert Sans (Google Fonts).

## La pub vidéo (livrée)

Objectif : produire seul, sans intervention de la propriétaire, une pub de 45 à 60 s en 16:9, la monter avec musique, **sans voix off** (décision de la propriétaire, 19 octobre 2026), et livrer `video/pub.mp4` prêt pour le site.

### Décisions prises

- [x] **Option B, version 50 s** (décision de la propriétaire, 19 octobre 2026) : 4 plans animés, plans fixes et cartons animés pour compléter, **sans voix off**, dans les 50 crédits de l'offre gratuite.

### Étapes (faites le 19 octobre 2026)

1. [x] Solde vérifié (50 crédits) ; le réseau joint les fichiers Higgsfield (`d8j0ntlcm91z4.cloudfront.net`).
2. [x] Portrait de Camille (`soul_2`) puis images de départ (`seedream_v5_lite` avec références). Sur l'offre gratuite : une génération à la fois, `gpt_image_2_5` et `nano_banana` refusés.
3. [x] 4 plans animés en `wan3_0` 720p, 5 s, sans son, tous réussis au premier essai.
4. [x] `pub/journal-generations.md` à jour ; sources dans `pub/rendus/` (images en JPEG).
5. [x] Pas de voix off : les phrases du script s'affichent à l'écran.
6. [x] Musique originale composée en code : `pub/musique.py`.
7. [x] Montage en code : `pub/montage.py` (cartons, bulles, légendes, soleil, encodage).
8. [x] `video/pub.mp4` : 50 s, H.264 High, yuv420p, 1280×720, 25 i/s, AAC 128 kb/s, faststart, 7,7 Mo.
9. [x] `images/video-poster.jpg` tirée du plan 4 (Camille à son bureau ; la propriétaire n'aimait pas le gros plan du plan 6) ; `og-image.jpg` inchangée (déjà bonne).
10. [x] Vérifié dans Chromium (copie WebM) : pas de défilement horizontal de 360 à 1920 px, lecture, retour au poster à la fin.
11. [x] Branche poussée, pull request ouverte.

Total dépensé : 42,24 crédits ; solde restant environ 7,76.

### Refaire le montage

```
python3 pub/musique.py TRAVAIL/musique.wav
python3 pub/montage.py TRAVAIL video/pub.mp4
```

`TRAVAIL` est un dossier temporaire contenant `fonts/` avec `YoungSerif.ttf`, `AlbertSans-Medium.ttf` et `AlbertSans-Bold.ttf` (Google Fonts, format TTF). `IMAGE=12.3 python3 pub/montage.py TRAVAIL test.png` exporte une seule image pour vérifier. Les textes et la durée de chaque séquence sont en bas de `pub/montage.py`.

## Conventions

- Commits en français. Ne pas pousser directement sur `main`.
- Ne jamais dépenser de crédits Higgsfield au-delà du budget validé par la propriétaire ; annoncer le coût avant toute génération payante non prévue.
