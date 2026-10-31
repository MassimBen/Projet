"""@bruin
name: cnam.professionelle
type: python
image: python:3.11
connection: cnam

materialization:
  type: table
  strategy: create+replace

columns:
  - name: annee
    type: integer
  - name: profession_sante
    type: string
  - name: region
    type: string
  - name: libelle_region
    type: string
  - name: departement
    type: string
  - name: libelle_departement
    type: string
  - name: nombre_patients_medecin_traitant
    type: integer
  - name: taux_evolution_annuel
    type: string
  - name: taux_evolution_annuel_integer
    type: float
@bruin"""


from io import StringIO
import polars as pl
import requests


API_URL = (
    "https://data.ameli.fr/api/explore/v2.1/catalog/datasets/"
    "patientele-medecintraitant-generalistes-annuelle/exports/csv"
    "?use_labels=false&delimiter=%3B"
)

COLUMN_TYPES = {
    "annee": pl.Int64,
    "profession_sante": pl.Utf8,
    "region": pl.Utf8,
    "libelle_region": pl.Utf8,
    "departement": pl.Utf8,
    "libelle_departement": pl.Utf8,
    "nombre_patients_medecin_traitant": pl.Int64,
    "taux_evolution_annuel": pl.Utf8,
    "taux_evolution_annuel_integer": pl.Float64
}

def materialize_professionelle() -> pl.DataFrame:
    response = requests.get(API_URL, timeout=(10,120))
    response.raise_for_status()

    data = pl.read_csv(
        StringIO(response.text),
        separator=";",
        dtypes=COLUMN_TYPES,
    )
    missing_columns = set(COLUMN_TYPES).difference(data.columns)
    if missing_columns:
        raise ValueError("L'API professionnelle de santé ne contient pas les colonnes attendues : "
            + ", ".join(sorted(missing_columns)))
    if data.is_empty():
        raise ValueError("L'API professionnelle de santé ne contient pas de données.")
    
    return data.select(list(COLUMN_TYPES))