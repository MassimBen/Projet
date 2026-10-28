variable "project" {
  description = "ID projet"
  type        = string
  default     = "cnam-pipeline"
}

variable "region" {
  description = "Region default des ressource GCP"
  type        = string
  default     = "europe-west1"
}

variable "location" {
  description = "localisation géographique"
  type        = string
  default     = "EU"
}