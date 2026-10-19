# Nouveau Lundi

Site vitrine one-page statique (HTML, CSS, JS, sans build) d'un organisme de formation fictif à l'IA générative pour les fonctions support. Hébergé sur GitHub Pages depuis `main`, dossier racine. La propriétaire du projet n'est pas technique : lui répondre en français, simplement, et ne lui demander une action que si personne d'autre ne peut la faire (achat, réglage de compte).

## Structure

- `index.html`, `css/styles.css`, `js/main.js` : le site, fidèle à la maquette « Grand jour » de Claude Design. Mobile sous 760 px (container queries sur `.page`).
- `video/pub.mp4` : la pub. Pour l'instant une vidéo placeholder de 6 s. Le lecteur est une balise `<video>` native (poster, bouton de la maquette, contrôles natifs après le clic) : remplacer le fichier suffit, aucun code à changer.
- `images/` : placeholders (poster de la vidéo, photos, témoignages, image Open Graph). Voir `images/README.md`.
- `pub/storyboard.md` : concept, direction artistique, script et prompts de la pub.
- `pub/lecons-projet-precedent.md` : règles et coûts tirés d'un autre projet Higgsfield. À respecter.
- Chemins relatifs uniquement (le site est servi depuis un sous-dossier). `og:url` et `og:image` pointent vers `https://fzlaa.github.io/new-monday/`.

Palette : crème `#FDFAF3`, vert encre `#0F241D`, abricot `#FE9979`, abricot clair `#FFC282`, menthe `#ACE7CC`, pêche `#FDD4C6`, beurre `#FBEFC2`. Polices : Young Serif et Albert Sans (Google Fonts).

## Ce qui reste à faire : la pub vidéo

Objectif : produire seul, sans intervention de la propriétaire, une pub de 45 à 60 s en 16:9, la monter avec musique et voix off, et livrer `video/pub.mp4` prêt pour le site.

### Décisions en attente (à demander en une seule question si elles ne sont pas déjà prises)

- [ ] **Option A** (film complet, 6 plans générés, 46 s, environ 100 crédits avec 25 % de réserve ; version longue d'environ 60 s possible avec 2 ou 3 plans de plus) ou **option B** (4 plans générés, cartons animés, environ 40 s, sous 50 crédits). L'option A demande l'offre Higgsfield Starter (270 crédits), que seule la propriétaire peut acheter. Solde au 19 octobre 2026 : 50 crédits, offre gratuite.

### Étapes

1. [ ] Vérifier le solde Higgsfield (connecteur Higgsfield, outil `balance`) et que le réseau de la session joint les fichiers Higgsfield : `curl -sS -o /dev/null -w "%{http_code}" https://d2ol7oe51mr4n9.cloudfront.net/` (000 = bloqué). Si c'est bloqué, ajouter le domaine aux domaines autorisés de l'environnement, ou faire le montage dans le bac à sable Higgsfield (`sandbox_exec`, qui a ffmpeg et Internet) et livrer un lien de téléchargement. Les résultats de génération peuvent venir d'un autre hôte CloudFront : vérifier l'URL du premier résultat.
2. [ ] Générer le portrait de Camille, puis les images de départ (règles de `pub/lecons-projet-precedent.md` : modèle d'édition d'image avec référence, phrase de continuité, négatif commun, « only one woman in the frame »). Toujours `get_cost` avant de générer et rester dans le budget validé.
3. [ ] Animer chaque plan en **Wan 3.0** (`wan3_0`), 720p, 16:9, durée du script. Réduction de 60 % jusqu'au 31 octobre 2026. Caméra fixe ou léger travelling avant. Une prise par plan, une seconde seulement si la première rate.
4. [ ] Tenir `pub/journal-generations.md` à jour (prompt, modèle, coût, résultat, gardé ou non) et télécharger chaque résultat tout de suite dans `pub/rendus/` (hors dépôt si trop lourd).
5. [ ] Voix off française avec `seed_audio` (environ 1,7 crédit pour tout le texte, voir le script).
6. [ ] Musique : le connecteur Higgsfield n'autorise pas la génération de musique seule. La composer en code (originale, libre de droits) : pizzicati et piano hésitants pour le lundi d'avant, même mélodie enjouée pour le lundi d'après, accord final.
7. [ ] Montage ffmpeg : couper les plans, fondus, bulles (Young Serif, coins arrondis 44 px, un coin pointu, pêche ou menthe), « Lundi d'avant » / « Lundi d'après », carton final animé (soleil abricot qui se lève derrière « Nouveau Lundi », puis « À lundi ? » et nouveaulundi.fr). Mixer voix et musique (`loudnorm`).
8. [ ] Export pour le site : H.264 High, `yuv420p`, 1280×720, 25 i/s, AAC 128 kb/s stéréo, `-movflags +faststart`, moins de 25 Mo (viser environ 7 Mo). Remplacer `video/pub.mp4`.
9. [ ] Nouvelle image d'aperçu `images/video-poster.jpg` (1920×1080) tirée du plan 6, et mettre à jour `images/og-image.jpg` si besoin.
10. [ ] Vérifier dans Chromium headless (Playwright est préinstallé ; il ne lit pas le H.264, tester la logique avec une copie WebM) : pas de défilement horizontal de 360 à 1920 px, lecture et retour au poster à la fin.
11. [ ] Committer sur une branche, pousser, ouvrir une pull request vers `main`, et donner à la propriétaire un résumé simple avec le lien.

## Conventions

- Commits en français. Ne pas pousser directement sur `main`.
- Ne jamais dépenser de crédits Higgsfield au-delà du budget validé par la propriétaire ; annoncer le coût avant toute génération payante non prévue.
