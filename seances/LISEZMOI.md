# Séances

Un dossier = une séance. Le site se reconstruit tout seul à chaque dépôt (onglet **Actions** du dépôt : pastille verte = en ligne, environ 2 min ; rouge = cliquer dessus, le message dit quel fichier corriger).

```
seances/
  courses.json                       les 4 cours (titre, niveau, ordre d'affichage)
  e-music-ma/                        un dossier par cours : e-music-ma, e-music-ba, interfaces, concepts-et-creation
    2026-11-24-simple-spat-02/       AAAA-MM-JJ-mots-en-minuscules
      simple_spat_02.md              le texte de la page (un seul .md par dossier)
      simple_spat_02.maxpat          le patch
      config.json                    patch, zones, pastilles, viewBox, démos
      spat_oper.png                  images éventuelles
```

**Ajouter une séance** : sur GitHub, ouvrir le dossier du cours (ex. `seances/e-music-ma`), puis **Add file › Upload files**, glisser le dossier de la séance, **Commit changes**.

**Corriger une séance** : remplacer le fichier de la même manière (ou cliquer sur le `.md` puis sur le crayon pour le modifier en ligne).

**Séance partagée entre deux cours** : la ranger dans le premier cours et ajouter dans l'en-tête du `.md` la ligne `aussi: e-music-ba` (plusieurs cours : `aussi: [e-music-ba, interfaces]`).

**Brouillon** : un dossier dont le nom commence par `_` (ex. `_2026-12-08-granular`) est ignoré.
