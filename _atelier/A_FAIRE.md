# À faire

## Construction automatique (GitHub Actions) — mise en place le 25.11.2026

Fait : sources dans `seances/<cours>/<AAAA-MM-JJ-slug>/`, `seances/courses.json`, `build.py` qui découvre les séances (champ `aussi:` pour une séance partagée), workflow `.github/workflows/pages.yml` (build + PDF + déploiement). Sortie vérifiée identique au site publié jusqu'ici.

Reste à faire par l'enseignant :

1. Settings › Pages › Build and deployment › Source : « GitHub Actions ».
2. Vérifier le premier déploiement (onglet Actions, pastille verte) puis le site.
3. Ensuite seulement, supprimer de la racine les anciennes pages générées : `index.html`, `assets/`, `notions/`, `e-music-ma/`, `e-music-ba/`, `interfaces/`, `concepts-et-creation/`, et les anciens essais `v2/`, `v2c/`, `v2d/`, `v2new/` (ils ne sont plus publiés).

Option : connecter GitHub à Claude (accès push au dépôt) pour que Claude dépose lui-même les nouveaux dossiers de séance.

## Idées en attente

Extrait audio par patch. Renommer éventuellement le dépôt en `emc-studio.github.io` pour une adresse courte.

## État

Deux séances : e-music-ma/2026-11-10-i-am-sitting-in-a-room (aussi e-music-ba) ; e-music-ma/2026-11-24-simple-spat-02. Documents sources : « Simple spat 02 · texte de la page » et « I am sitting in a room · texte de la page » (Claude Docs).
