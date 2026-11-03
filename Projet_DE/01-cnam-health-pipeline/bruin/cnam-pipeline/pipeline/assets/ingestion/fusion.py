dossier = r"D:\Pipeline_ELT_gcp\Projet\Projet_DE\01-cnam-health-pipeline\bruin\cnam-pipeline\pipeline\assets\ingestion"

with open(dossier + r"\NTOT2025_janvier_avril.CSV", "wb") as sortie:
    for mois in range(1, 5):
        nom = dossier + rf"\NTOT2025_{mois:02d}.CSV"

        with open(nom, "rb") as fichier:
            if mois == 1:
                sortie.write(fichier.readline())  
            else:
                fichier.readline()  

            sortie.writelines(fichier)

print("Fusion terminée.")