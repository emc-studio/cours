# Atelier EMC Studio

Les sources qui génèrent ce site. Rien ici n'est à modifier à la main : le texte de chaque séance vient de son document Markdown (`src/<cours>/<séance>/*.md`).

- `src/site.json` : la liste des cours et de leurs séances
- `src/<cours>/<séance>/` : le texte (`.md`), le patch (`.maxpat`), les images et `config.json` (pastilles du patch, démos)
- `assets/` : la feuille de style commune et les polices (OFL)
- `build.py` + `session.js` + `search.js` : le générateur — `python3 build.py src out assets`
- `pdf.py` : les PDF imprimables — `python3 pdf.py out`
