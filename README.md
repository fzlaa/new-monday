# Nouveau Lundi

Site vitrine one-page de Nouveau Lundi, organisme de formation (fictif) à l'IA générative pour les fonctions support. Il implémente la maquette « Grand jour » réalisée dans Claude Design.

Site statique en HTML, CSS et JavaScript, sans framework ni étape de build. Pour le voir, il suffit d'ouvrir `index.html` dans un navigateur. Tous les chemins sont relatifs, donc le site fonctionne aussi depuis un sous-dossier (`pseudo.github.io/nouveau-lundi/`).

```
├── index.html
├── css/styles.css
├── js/main.js
├── images/        placeholders à remplacer (voir images/README.md)
├── video/pub.mp4  vidéo placeholder à remplacer
├── favicon.ico
└── .nojekyll
```

## Remplacer la vidéo

1. Compressez la publicité en MP4 H.264 + AAC, avec une taille cible sous 25 Mo pour 60 s :

   ```sh
   ffmpeg -i ma-pub.mov \
     -c:v libx264 -profile:v high -preset slow -crf 23 \
     -maxrate 2800k -bufsize 5600k \
     -vf "scale='min(1920,iw)':-2,format=yuv420p" \
     -c:a aac -b:a 128k -ac 2 \
     -movflags +faststart \
     video/pub.mp4
   ```

   `-maxrate 2800k` limite le débit vidéo : 60 s donnent environ 22 Mo. Si le fichier dépasse encore 25 Mo, baissez `-maxrate` (par exemple à `2200k`). `-movflags +faststart` permet de démarrer la lecture avant la fin du téléchargement.

2. Remplacez `video/pub.mp4` par ce fichier, sous le même nom. Aucun code n'est à modifier.

3. Facultatif : remplacez l'image d'aperçu par une image tirée du film, par exemple à la 3e seconde :

   ```sh
   ffmpeg -ss 3 -i video/pub.mp4 -frames:v 1 -vf scale=1920:-2 -q:v 3 images/video-poster.jpg
   ```

Vérifiez la taille avec `ls -lh video/pub.mp4`. GitHub refuse les fichiers de plus de 100 Mo.

## Activer GitHub Pages

1. Fusionnez cette branche dans `main`.
2. Sur GitHub, ouvrez le dépôt, puis **Settings → Pages**.
3. Dans **Build and deployment**, choisissez **Source : Deploy from a branch**, puis la branche **`main`** et le dossier **`/ (root)`**. Cliquez sur **Save**.
4. Après une à deux minutes, le site est en ligne à l'adresse `https://<pseudo>.github.io/<nom-du-depot>/` (ici https://fzlaa.github.io/new-monday/).

Le fichier `.nojekyll` indique à GitHub Pages de servir les fichiers tels quels, sans passer par Jekyll.

Open Graph exige des URL absolues. Si l'adresse du site change (dépôt renommé, nom de domaine), mettez à jour `og:url` et `og:image` dans `index.html`.
