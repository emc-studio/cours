# Séances

Un dossier = une séance. Le site se reconstruit tout seul à chaque dépôt (onglet **Actions** du dépôt : pastille verte = en ligne, environ 1 min ; rouge = cliquer dessus, le message dit quel fichier corriger).

```
seances/
  courses.json                          les cours (nom du dossier, titre, niveau, ordre d'affichage)
  2026-11-24-simple-spat-02/            une séance : AAAA-MM-JJ-mots-en-minuscules
    simple_spat_02.md                   le texte de la page (un seul .md par dossier)
    simple_spat_02.maxpat               le patch
    config.json                         patch, zones, pastilles, viewBox, démos
    spat_oper.png                       images éventuelles
```

**Le cours se choisit dans l'en-tête du `.md`**, avec les noms de `courses.json` :

```
cours: e-music-ma                       un seul cours
cours: e-music-ma, e-music-ba           la même page dans les deux cours (le premier est le cours principal)
```

Le titre et le niveau affichés (« Musique électronique MA · BA », « master · bachelor ») sont écrits automatiquement.

**Rangement libre** : les dossiers de séance peuvent être directement dans `seances/` ou dans des sous-dossiers (par thème, par année…). L'adresse de la page ne dépend que du nom du dossier de la séance : `…/2026-11-24-simple-spat-02/`. Réorganiser ne casse aucun lien. Deux séances ne peuvent pas porter le même nom.

**Ajouter une séance** : sur GitHub, ouvrir `seances`, puis **Add file › Upload files**, glisser le dossier de la séance, **Commit changes**.

**Corriger une séance** : cliquer sur le `.md`, puis sur le crayon pour le modifier en ligne (ou remplacer le fichier par Upload files).

**Brouillon** : un dossier dont le nom commence par `_` (ex. `_brouillons/`) est ignoré, avec tout ce qu'il contient.
