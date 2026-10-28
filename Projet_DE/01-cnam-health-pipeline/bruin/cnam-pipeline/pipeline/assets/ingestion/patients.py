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
  - name: patho_niv1
    type: string
  - name: patho_niv2
    type: string
  - name: patho_niv3
    type: string
  - name: top
    type: string
  - name: comorbidite
    type: string
  - name: libelle_comorbidite
    type: string
  - name: region
    type: integer
  - name: dept
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

import pandas as pd
import requests

API_URL = (
    "https://data.ameli.fr/api/explore/v2.1/catalog/datasets/"
    "comorbidites/exports/csv?use_labels=false&delimiter=%3B"
)

COLUMN_TYPES = {
    "annee": "Int64",
    "patho_niv1": "string",
    "patho_niv2": "string",
    "patho_niv3": "string",
    "top": "string",
    "comorbidite": "string",
    "libelle_comorbidite": "string",
    "region": "Int64",
    "dept": "Int64",
    "ncomorb": "Int64",
    "ntop": "Int64",
    "proportion_comorb": "Float64",
    "patho_niv1_comorb": "string",
    "patho_niv2_comorb": "string",
    "patho_niv3_comorb": "string",
    "niveau_prioritaire": "string",
}


def materialize() -> pd.DataFrame:
    response = requests.get(API_URL, timeout=(10, 120))
    response.raise_for_status()

    data = pd.read_csv(
        StringIO(response.text),
        sep=";",
        dtype=COLUMN_TYPES,
    )
    missing_columns = set(COLUMN_TYPES).difference(data.columns)
    if missing_columns:
        raise ValueError(
            "L'API Comorbidités ne contient pas les colonnes attendues : "
            + ", ".join(sorted(missing_columns))
        )
    if data.empty:
        raise ValueError("L'API Comorbidités a renvoyé un jeu de données vide.")

    return data[list(COLUMN_TYPES)]
