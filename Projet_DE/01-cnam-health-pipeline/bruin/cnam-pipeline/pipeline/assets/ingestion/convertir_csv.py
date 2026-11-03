import csv
from pathlib import Path

dossier = Path(
    r"D:\Pipeline_ELT_gcp\Projet\Projet_DE\01-cnam-health-pipeline"
    r"\bruin\cnam-pipeline\pipeline\assets\ingestion"
)

source = dossier / "NTOT2025_janvier_avril.CSV"
destination = dossier / "NTOT2025_janvier_avril_seed.csv"

lignes = 0

with source.open("r", encoding="cp1252", newline="") as entree, \
     destination.open("w", encoding="utf-8", newline="") as sortie:

    lecteur = csv.reader(entree, delimiter=";", strict=True)
    redacteur = csv.writer(
        sortie,
        delimiter=",",
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )

    for ligne in lecteur:
        redacteur.writerow(ligne)
        lignes += 1

print(f"Conversion terminée : {lignes} lignes écrites dans {destination.name}")