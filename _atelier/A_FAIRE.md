# Chantier suivant : construction automatique du site (GitHub Actions)

Objectif : l'enseignant (ou Claude) dépose seulement le dossier d'une nouvelle séance ; GitHub construit et publie le site tout seul.

1. Réorganiser le dépôt : les sources dans `seances/<cours>/<AAAA-MM-JJ-slug>/` (texte `.md`, `.maxpat`, images, `config.json`) ; `courses.json` pour les 4 cours (titre, niveau, ordre) ; le générateur (`build.py`, `pdf.py`, `session.js`, `search.js`, `assets/`) dans `_atelier/`.
2. `build.py` découvre les séances en lisant les sous-dossiers (plus de liste de séances dans `site.json`). Séance partagée : champ `aussi: e-music-ba` dans l'en-tête du `.md`.
3. Ajouter `.github/workflows/pages.yml` : à chaque push → Python + `markdown` + `pyyaml` + Playwright (Chromium) → `build.py` puis `pdf.py` → `actions/upload-pages-artifact` → `actions/deploy-pages`.
4. L'enseignant passe Settings › Pages › Source sur « GitHub Actions ».
5. Supprimer de la racine les pages générées (index.html, assets/, notions/, dossiers de cours) une fois le premier déploiement réussi.
6. Option : connecter GitHub à Claude (add_repo, accès push) pour que Claude dépose lui-même les nouveaux dossiers.

État au 25.11.2026 : deux séances en ligne (e-music-ma/2026-11-10-i-am-sitting-in-a-room, partagée avec e-music-ba ; e-music-ma/2026-11-24-simple-spat-02). Documents sources : « Simple spat 02 · texte de la page » et « I am sitting in a room · texte de la page » (Claude Docs).
