# Pipeline de données CNAM

## Présentation

Ce projet met en place un pipeline ELT avec Bruin et Google Cloud Platform. Il charge dans BigQuery :

- des données mensuelles de dépenses de santé CNAM téléchargées manuellement ;
- des données de comorbidités récupérées depuis l'API Data ameli ;
- des données annuelles de patientèle des médecins traitants récupérées depuis l'API Data ameli.

La destination BigQuery est le dataset `cnam`, dans le projet GCP `cnam-pipeline`.

## Sources de données

### Dépenses 2025 — fichiers CSV

Les fichiers de dépenses ne sont pas récupérés par une API dans ce projet : ils doivent être téléchargés depuis les pages officielles de l'Assurance Maladie.

- [Dépenses d'assurance maladie](https://www.assurance-maladie.ameli.fr/etudes-et-donnees/par-theme/depenses-assurance-maladie)
- [Catalogue des données en open data (Excel et CSV)](https://www.assurance-maladie.ameli.fr/etudes-et-donnees/donnees/liste-donnees-open-data)

Depuis le catalogue, choisir la série de données de dépenses correspondant au périmètre souhaité, puis télécharger les fichiers mensuels de 2025. Le pipeline actuellement configuré utilise les mois de janvier à avril : les fichiers attendus sont ceux correspondant aux mois `01` à `04` (`NTOT2025_01.CSV` à `NTOT2025_04.CSV`). Vérifier la période, le régime et le périmètre proposés par la page source avant le téléchargement, car les fichiers publiés peuvent évoluer.

Les fichiers doivent rester localement dans le dossier d'ingestion :

[`bruin/cnam-pipeline/pipeline/assets/ingestion/`](./bruin/cnam-pipeline/pipeline/assets/ingestion/)

Ils ne doivent pas être ajoutés au dépôt Git. Les motifs de fichiers de dépenses sont exclus des futurs ajouts par le `.gitignore` à la racine du dossier `Projet`. Cette règle n'enlève toutefois pas du suivi Git des fichiers déjà commités ou déjà suivis par Git LFS.

### Comorbidités — asset `cnam.comorbidites`

- Fiche du jeu de données : [Comorbidités associées aux pathologies](https://data.ameli.fr/explore/dataset/comorbidites/information/)
- API CSV utilisée par [`patients.py`](./bruin/cnam-pipeline/pipeline/assets/ingestion/patients.py) :
  [Exporter les données de comorbidités](https://data.ameli.fr/api/explore/v2.1/catalog/datasets/comorbidites/exports/csv?use_labels=false&delimiter=%3B)
- Le séparateur fourni par cette API est le point-virgule.

### Patientèle des médecins traitants — asset `cnam.professionelle`

- Fiche du jeu de données : [Patientèle médecin traitant généralistes annuelle](https://data.ameli.fr/explore/dataset/patientele-medecintraitant-generalistes-annuelle/information/)
- API CSV utilisée par [`professionelle.py`](./bruin/cnam-pipeline/pipeline/assets/ingestion/professionelle.py) :
  [Exporter les données de patientèle](https://data.ameli.fr/api/explore/v2.1/catalog/datasets/patientele-medecintraitant-generalistes-annuelle/exports/csv?use_labels=false&delimiter=%3B)
- Le séparateur fourni par cette API est le point-virgule.

Ces deux assets interrogent directement leur API lors de l'exécution ; il n'est pas nécessaire de télécharger ces jeux de données à l'avance.

## Préparation des dépenses CSV

1. Télécharger depuis le portail officiel les fichiers mensuels nécessaires pour 2025 et les placer dans le dossier d'ingestion indiqué ci-dessus.
2. Vérifier que les fichiers téléchargés sont complets, ont le bon mois et partagent le même format et les mêmes colonnes.
3. Fusionner les fichiers mensuels en conservant l'en-tête une seule fois.
4. Convertir le résultat vers le format CSV attendu par l'asset seed : les fichiers source utilisent des points-virgules, tandis que le fichier de seed doit être lisible par son chargeur avec le dialecte attendu. La conversion doit préserver les accents et l'échappement des guillemets. Conserver les sources mensuelles et le fichier fusionné comme données locales.
5. Vérifier que le fichier final existe sous le nom configuré dans [`NTOT_2025_lookup.asset.yml`](./bruin/cnam-pipeline/pipeline/assets/ingestion/NTOT_2025_lookup.asset.yml) : `NTOT2025_janvier_avril_seed.csv`.
6. Contrôler le fichier converti en entier et comparer son nombre de lignes avec les fichiers mensuels avant d'exécuter l'asset.

> **Cohérence des noms :** le périmètre actuel couvre janvier à avril. La fusion produit `NTOT2025_janvier_avril.CSV`, la conversion produit `NTOT2025_janvier_avril_seed.csv` et l'asset seed attend ce dernier nom. Conserver cette cohérence si le périmètre ou les noms de fichiers changent.

## Étapes du projet

### 1. Préparer l'environnement local

- Installer Google Cloud SDK et Bruin CLI.
- Disposer de Python 3.11 pour les assets Python.
- Depuis le dossier `bruin/cnam-pipeline`, utiliser la configuration du pipeline et les dépendances Python déclarées dans le dossier d'ingestion.
- Les fichiers locaux de configuration et les journaux d'exécution ne doivent pas contenir ni exposer de secrets.

### 2. Configurer Google Cloud et BigQuery

Le projet GCP est `cnam-pipeline`. Le dataset BigQuery est `cnam`, avec une localisation `EU`.

La configuration Terraform du dossier [`terraform/`](./terraform/) déclare le dataset BigQuery. L'authentification locale repose sur les Application Default Credentials du Google Cloud SDK. Configurer l'identité GCP avant l'exécution du pipeline.

Le compte de service utilisé pour le pipeline doit avoir :

- le rôle **BigQuery Job User** (`roles/bigquery.jobUser`) au niveau du projet ;
- les droits de lecture et d'écriture sur le dataset `cnam`, notamment **BigQuery Data Editor** (`roles/bigquery.dataEditor`).

La configuration IAM décrite ici est actuellement faite manuellement dans la console GCP ; elle n'est pas créée par les fichiers Terraform présents dans le projet.

### 3. Préparer et vérifier les données

- Télécharger et préparer localement les CSV de dépenses, sans les commiter.
- Vérifier l'accès réseau aux API Data ameli des deux assets Python.
- Vérifier dans chaque asset la cohérence entre colonnes, types attendus et schéma de destination.

### 4. Valider et exécuter le pipeline

- Lancer la validation Bruin depuis le dossier du pipeline. La validation vérifie la configuration, mais ne garantit pas que le CSV complet peut être lu ni que les API répondent correctement.
- Exécuter d'abord un asset isolément pour diagnostiquer sa source et sa destination, puis lancer les assets nécessaires du pipeline.
- Consulter le journal Bruin et le résumé JSON de chaque exécution ; conserver les erreurs et résultats utiles dans [`learning.md`](../../learning.md).

Le seed de dépenses utilise une stratégie de remplacement de table. Vérifier l'asset ciblé et l'environnement avant de lancer une exécution qui écrit dans BigQuery.

### 5. Contrôler les résultats BigQuery

Après une exécution réussie, vérifier dans le dataset `cnam` la présence et le volume des tables :

| Asset Bruin | Table cible |
|---|---|
| `cnam.depenses_2025` | `cnam.depenses_2025` |
| `cnam.comorbidites` | `cnam.comorbidites` |
| `cnam.professionelle` | `cnam.professionelle` |

Comparer les nombres de lignes et les colonnes obtenus aux sources et aux schémas déclarés dans les assets.

## Organisation du dépôt

- [`bruin/cnam-pipeline/pipeline/pipeline.yml`](./bruin/cnam-pipeline/pipeline/pipeline.yml) : identité du pipeline et connexion GCP par défaut.
- [`bruin/cnam-pipeline/pipeline/assets/ingestion/`](./bruin/cnam-pipeline/pipeline/assets/ingestion/) : définitions d'assets, scripts d'ingestion et dépendances.
- [`terraform/`](./terraform/) : configuration du dataset BigQuery.
- [`logs/`](./logs/) : journaux et résumés des exécutions locales ; ces fichiers sont exclus du suivi Git.
- [`../../learning.md`](../../learning.md) : journal des incidents, diagnostics et solutions envisagées ou appliquées.

## Points de vigilance

- Ne pas ajouter les grands CSV de dépenses ni les exports générés au dépôt Git. Les récupérer depuis la source officielle et les garder localement.
- `.gitignore` ne désindexe pas les fichiers déjà suivis. Retirer des données déjà commitées ou suivies par Git LFS nécessite une opération Git distincte et une vérification de l'historique.
- Une erreur HTTP, une modification de schéma de l'API ou un changement du séparateur peut faire échouer les assets Python ; consulter le journal du run pour le message détaillé.
- Les fichiers mensuels peuvent être volumineux : prévoir suffisamment d'espace disque et vérifier les téléchargements avant fusion.
- Les pages et données sources officielles peuvent changer ; confirmer le millésime et les définitions de données au moment du téléchargement.
