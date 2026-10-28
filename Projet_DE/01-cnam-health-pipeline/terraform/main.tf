# ============================================
# DATASET BIGQUERY AVEC PARTAGE EXPLICITE
# ============================================

resource "google_bigquery_dataset" "cnam" {
  dataset_id  = "cnam"
  description = "Données CNAM - tables brutes, staging et marts"
  location    = var.location
}