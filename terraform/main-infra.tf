provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  repository_id = "parking-repo"
  format        = "DOCKER"
  location      = var.region

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_firestore_database" "default" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  lifecycle {
    prevent_destroy = true
  }
}
