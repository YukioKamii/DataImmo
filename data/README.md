# Données locales

Ce dossier est volontairement exclu du dépôt Git, à l'exception de ce fichier
et des `.gitkeep`.

## Organisation

```text
data/
├── raw/          # fichiers DVF téléchargés (.csv / .csv.gz)
└── processed/    # fichiers Parquet générés par le pipeline
```

## Pourquoi les données ne sont-elles pas versionnées ?

Les fichiers DVF sont volumineux et disponibles publiquement en open data.
Le dépôt contient donc uniquement le code permettant de les récupérer et de
reproduire le traitement.

## Récupérer un département

Depuis la racine du projet :

```bash
python scripts/download_dvf.py --year 2024 --department 59
```

Le fichier sera créé dans `data/raw/2024/59.csv.gz`.
