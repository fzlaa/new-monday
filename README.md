# Nouveau Lundi

Site vitrine one-page de Nouveau Lundi, organisme de formation (fictif) à l'IA générative pour les fonctions support. Il implémente la maquette « 1c Grand jour » faite dans Claude Design.

Site statique HTML/CSS/JS, sans dépendance ni étape de build.

## Lancer en local

```sh
python3 -m http.server
```

puis ouvrir http://localhost:8000.

## Structure

- `index.html` : contenu de la page
- `assets/css/styles.css` : styles. La version mobile s'affiche sous 760 px de large.
- `assets/js/main.js` : apparitions au scroll, menu mobile, lecteur vidéo, témoignages, FAQ
- `video/pub.mp4` : publicité de 1 min en 16:9, à déposer (voir `video/README.md`)
- `images/` : photos à déposer (voir `images/README.md`)
