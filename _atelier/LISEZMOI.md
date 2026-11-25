# Atelier EMC Studio

Générateur du site. Les séances sont dans `../seances/` (voir `seances/LISEZMOI.md`).

Publication : automatique, par GitHub Actions (`.github/workflows/pages.yml`) à chaque modification de la branche `main`. Relancer à la main : onglet Actions › Publier le site › Run workflow.

Construire en local (depuis la racine du dépôt) :

```
pip install -r _atelier/requirements.txt && python3 -m playwright install chromium
python3 _atelier/build.py seances _site _atelier/assets
python3 _atelier/pdf.py _site
```

`build.py` découvre les séances en lisant les sous-dossiers de `seances/<cours>/` et s'arrête avec un message en français si un dossier est mal formé (nom, en-tête, config.json, patch manquant, cours inconnu dans `aussi:`).

Suite : voir `A_FAIRE.md`.
