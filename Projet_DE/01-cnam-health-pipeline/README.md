
## 🔐 Accès et permissions

### Prérequis

| Élément | Valeur |
|---------|--------|
| Projet GCP | `cnam-pipeline` |
| Dataset BigQuery | `cnam` |
| Compte de service | `cnam-pipeline@cnam-pipeline.iam.gserviceaccount.com` |

### Rôles requis (configuration manuelle)

> **Choix assumé** : Les permissions IAM sont gérées via la console GCP pour garder le projet accessible et éviter la complexité Terraform inutile sur un environnement solo. Pour un déploiement multi-environnements, elles seraient migrées sous Terraform.

#### 1. Accès au projet (IAM & Administration → IAM)

| Principal | Rôle |
|-----------|------|
| `cnam-pipeline@cnam-pipeline.iam.gserviceaccount.com` | **Utilisateur de tâches BigQuery** (`roles/bigquery.jobUser`) |

> Permet de lancer des requêtes et des jobs de chargement.

#### 2. Accès au dataset (BigQuery → Dataset `cnam` → Partager)

| Principal | Rôle |
|-----------|------|
| `cnam-pipeline@cnam-pipeline.iam.gserviceaccount.com` | **Éditeur de données BigQuery** (`roles/bigquery.dataEditor`) |
| `cnam-pipeline@cnam-pipeline.iam.gserviceaccount.com` | **Lecteur de données BigQuery** (`roles/bigquery.dataViewer`) |

> **Éditeur** : lire, écrire et modifier les tables du dataset `cnam`.
> **Lecteur** : lire les tables et exécuter des requêtes `SELECT`.

### Méthode d'authentification : Google SDK (ADC)

> **Choix retenu** : Authentification via Application Default Credentials du Google Cloud SDK. La variable d'environnement `GOOGLE_APPLICATION_CREDENTIALS` pointe vers la clé JSON du compte de service.

```
$ gcloud auth application-default login
```

