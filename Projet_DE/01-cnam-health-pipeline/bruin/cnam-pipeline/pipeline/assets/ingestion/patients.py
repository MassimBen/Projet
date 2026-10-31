"""@bruin
name: cnam.comorbidites
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
    type: string
  - name: taux_evolution_annuel
    type: string
  - name: taux_evolution_annuel_integer
    type: integer
  - name: ncomorb
    type: integer
  - name: ntop
    type: integer
  - name: proportion_comorb
    type: float
  - name: patho_niv1_comorb
    type: string
  - name: patho_niv2_comorb
    type: string
  - name: patho_niv3_comorb
    type: string
  - name: niveau_prioritaire
    type: string
@bruin"""

from io import StringIO

import polars as pl
import requests

# data source: https://data.ameli.fr/explore/dataset/comorbidites/information/
API_URL = (
    "https://data.ameli.fr/api/explore/v2.1/catalog/datasets/"
    "comorbidites/exports/csv?use_labels=false&delimiter=%3B"
)
 # columns and their types as expected from the API response
COLUMN_TYPES = {
    "annee": pl.Int64,
    "patho_niv1": pl.String,
    "patho_niv2": pl.String,
    "patho_niv3": pl.String,
    "top": pl.String,
    "comorbidite": pl.String,
    "libelle_comorbidite": pl.String,
    "region": pl.Int64,
    "dept": pl.Int64,
    "ncomorb": pl.Int64,
    "ntop": pl.Int64,
    "proportion_comorb": pl.Float64,
    "patho_niv1_comorb": pl.String,
    "patho_niv2_comorb": pl.String,
    "patho_niv3_comorb": pl.String,
    "niveau_prioritaire": pl.String,
}

# function to fetch and materialize the data from the API
def materialize_comorbidites() -> pl.DataFrame:
    response = requests.get(API_URL, timeout=(10, 120))
    response.raise_for_status()
# data is read into a Polars DataFrame with specified column types
    data = pl.read_csv(
        StringIO(response.text),
        separator=";",
        dtypes=COLUMN_TYPES,
    )
    # check for missing columns and raise an error if any are missing
    missing_columns = set(COLUMN_TYPES).difference(data.columns)
    if missing_columns:
        raise ValueError(
            "L'API Comorbidités ne contient pas les colonnes attendues : "
            + ", ".join(sorted(missing_columns))
        )
    if data.is_empty():
        raise ValueError("L'API Comorbidités a renvoyé un jeu de données vide.")

    return data.select(list(COLUMN_TYPES))
