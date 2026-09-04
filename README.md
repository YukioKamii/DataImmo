# DataImmo — Livrable 1

Pipeline Python d'ingestion et de nettoyage des données **DVF géolocalisées**
pour un département français.

Ce premier livrable met en pratique **Python orienté objet + Pandas** : lecture
par chunks, nettoyage, calcul du prix au m² et export en Parquet.

## Fonctionnalités

- lecture d'un CSV DVF, compressé (`.csv.gz`) ou non ;
- lecture par chunks afin de limiter la mémoire utilisée pendant l'ingestion ;
- conversion des principaux types ;
- suppression des lignes sans prix ou sans surface bâtie ;
- suppression des doublons sur `id_mutation`, y compris entre deux chunks ;
- calcul de `prix_m2` ;
- filtrage des prix aberrants hors de l'intervalle 100–20 000 €/m² ;
- export du résultat au format Parquet ;
- rapport console avant/après nettoyage et mémoire utilisée.

## Architecture

```text
DataImmo/
├── data/
│   ├── raw/                  # données DVF locales, ignorées par Git
│   ├── processed/            # Parquet générés, ignorés par Git
│   └── README.md             # procédure de récupération des données
├── scripts/
│   └── download_dvf.py       # télécharge un département depuis data.gouv.fr
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # classe DataLoader
│   ├── data_cleaner.py       # classe DataCleaner
│   └── data_exporter.py      # classe DataExporter
├── .gitignore
├── main.py                   # orchestration du pipeline
├── requirements.txt
└── README.md
```

Cette organisation sépare les responsabilités :

- **DataLoader** s'occupe uniquement de l'ingestion ;
- **DataCleaner** applique les règles de nettoyage ;
- **DataExporter** s'occupe de la persistance ;
- **main.py** orchestre les trois étapes et affiche le rapport.

L'arborescence `data/` existe dans le dépôt pour documenter où placer les
fichiers, mais son contenu lourd n'est jamais versionné.

## Prérequis

- Python 3.10 ou supérieur
- Git

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd DataImmo
```

### 2. Créer un environnement virtuel

Sous Windows PowerShell :

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sous macOS / Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Récupération des données

Les données ne sont **pas stockées sur GitHub**. Elles sont récupérables depuis
la source publique Geo-DVF.

Exemple avec le département 59 pour l'année 2024 :

```bash
python scripts/download_dvf.py --year 2024 --department 59
```

Le fichier obtenu se trouve ici :

```text
data/raw/2024/59.csv.gz
```

URL construite par le script :

```text
https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/59.csv.gz
```

## Exécution du livrable 1

```bash
python main.py \
  --input data/raw/2024/59.csv.gz \
  --output data/processed/dvf_2024_59_clean.parquet
```

Sous PowerShell, la commande peut également être écrite sur une seule ligne :

```powershell
python main.py --input data/raw/2024/59.csv.gz --output data/processed/dvf_2024_59_clean.parquet
```

La taille d'un chunk peut être modifiée :

```bash
python main.py \
  --input data/raw/2024/59.csv.gz \
  --output data/processed/dvf_2024_59_clean.parquet \
  --chunk-size 50000
```

## Règles de nettoyage

Pour chaque chunk, le pipeline :

1. convertit `date_mutation` en date ;
2. convertit les colonnes numériques utiles ;
3. supprime les lignes sans `valeur_fonciere` ou `surface_reelle_bati` ;
4. supprime les surfaces nulles ou négatives ;
5. calcule `prix_m2 = valeur_fonciere / surface_reelle_bati` ;
6. conserve les transactions entre 100 et 20 000 €/m² inclus ;
7. conserve une seule ligne par `id_mutation`.

Le dédoublonnage mémorise les mutations déjà conservées afin de fonctionner
même lorsqu'un même identifiant apparaît dans deux chunks différents.

## Exemple de rapport

```text
=== Rapport DataImmo - Livrable 1 ===
Fichier source          : data/raw/2024/59.csv.gz
Lignes avant nettoyage  : ...
Lignes après nettoyage  : ...
Lignes supprimées       : ...
Mémoire max d'un chunk  : ... MiB
Mémoire données propres : ... MiB
Parquet généré          : data/processed/dvf_2024_59_clean.parquet
```

## Vérifier que le Parquet est lisible

```bash
python -c "import pandas as pd; df = pd.read_parquet('data/processed/dvf_2024_59_clean.parquet'); print(df.head()); print(df.shape)"
```

## Git et données

Les fichiers `.csv`, `.csv.gz` et `.parquet` sont explicitement ignorés dans
`.gitignore`. Avant chaque push, il est possible de vérifier qu'aucune donnée
n'est suivie par erreur :

```bash
git status
git ls-files data/
```

`git ls-files data/` ne doit afficher que les fichiers de documentation ou les
`.gitkeep`.

## Source des données

- Geo-DVF : https://files.data.gouv.fr/geo-dvf/latest/csv/
- Documentation du schéma DVF :
  https://github.com/datagouv/dvf/blob/master/README-CSV.md

## Suite du projet

Les livrables suivants pourront réutiliser les mêmes dossiers sans casser le
livrable 1. Spark, les agrégations nationales, les visualisations, l'API,
MinIO et MongoDB seront ajoutés progressivement dans leurs propres modules.
