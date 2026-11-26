# À faire

## Construction automatique (GitHub Actions) — mise en place le 25.11.2026

Fait : sources dans `seances/<cours>/<AAAA-MM-JJ-slug>/`, `seances/courses.json`, `build.py` qui découvre les séances (champ `aussi:` pour une séance partagée), workflow `.github/workflows/pages.yml` (build + PDF + déploiement). Sortie vérifiée identique au site publié jusqu'ici.

Réglage Pages passé sur « GitHub Actions », premier déploiement vérifié, anciennes pages générées supprimées de la racine (25.11.2026). Claude a l'accès en écriture au dépôt.

## Réorganisation du 26.11.2026

Séances directement dans `seances/` (rangement libre, sous-dossiers possibles), cours choisis dans l'en-tête du `.md` (`cours: e-music-ma, e-music-ba`), adresse de page indépendante du rangement : `<site>/<AAAA-MM-JJ-slug>/`. Dépôt renommé `emc-studio/cours` le 26.11.2026 : site à https://emc-studio.github.io/cours/ (liens à republier sur Discord).

## Prochains chantiers (décidés le 26.11.2026, rien de codé)

### 1. Années universitaires — un seul dépôt

Pas un dépôt par année (générateur en double, ressources coupées des séances, liens à republier chaque rentrée). L'année se déduit de la date de la séance (année universitaire : à partir d'août).
- Page d'un cours : séances regroupées par année universitaire, l'année en cours d'abord, les précédentes en dessous (repliées).
- Page d'accueil : l'année en cours mise en avant, lien « Années précédentes ».
- `courses.json` : pour chaque cours, les années où il est donné (un cours peut apparaître ou disparaître).
- Séance reprise telle quelle : ajouter la nouvelle date (champ à prévoir, ex. `donnee: [2026-11-10, 2027-11-09]`), la page et son adresse ne changent pas. Séance remaniée : nouvelle séance, l'ancienne reste en archive.
- Les adresses restent stables d'une année à l'autre.

### 2. Cours « Open Space »

Une ligne dans `seances/courses.json` (slug, titre, niveau).

### 3. Espace « Ressources » — commun à toutes les années

Onglet à part (pas un cours), relié aux séances :
- Une fiche courte par ressource : titre, auteur, type (livre, bibliothèque Max, pièce, vidéo, article, outil), lien, niveau conseillé, notions, quelques lignes de présentation dans le style de l'enseignant.
- Mêmes notions que les séances : la recherche et la page Notions & objets regroupent séances et ressources.
- Une séance cite une ressource dans sa section Ressources ; la fiche liste en retour les séances qui l'utilisent.
- Contenus envisagés : Puckette, *The Theory and Technique of Electronic Music* (en accès libre, renvois par chapitre en face des séances) ; sélection de bibliothèques Max (Spat 5, FluCoMa, MuBu, bach…) avec usage, installation, premier patch d'aide, séances liées ; pièces avec patchs (pièce, enregistrement, dispositif, lien vers le patch publié) ; fiches pratiques réutilisables (réglages audio de Max, quatre sorties au casque, déboguer un patch muet…), aujourd'hui répétées dans les encadrés des séances.
- YouTube : liens simples (avec `&t=85s` pour un moment précis) ; vidéo intégrée en youtube-nocookie seulement si la regarder fait partie de la séance.
- Droits : le site est en CC0 ; pour les œuvres d'autrui (livres, patchs, partitions), mettre un lien vers la source, ne pas recopier les fichiers.
- Option : vérification mensuelle automatique des liens externes (workflow), avec la liste des liens morts.
- Pour démarrer : lister 5 ou 6 ressources déjà citées en cours, fixer le format de fiche à partir de ces exemples.

## Idées en attente

Extrait audio par patch.

## État

Deux séances : 2026-11-10-i-am-sitting-in-a-room (e-music-ma, e-music-ba) ; 2026-11-24-simple-spat-02 (e-music-ma). Documents sources : « Simple spat 02 · texte de la page » et « I am sitting in a room · texte de la page » (Claude Docs).
