provider "google" {
  project = var.project_id
  region  = var.region
}

# Artifact Registry (for Docker images)
resource "google_artifact_registry_repository" "repo" {
  repository_id = "parking-repo"
  format        = "DOCKER"
  location      = var.region
}

# Cloud Run Service
resource "google_cloud_run_service" "parking_api" {
  name     = "parking-api"
  location = var.region

  template {
    spec {
      containers {
        image = var.image_url
        ports {
          container_port = 8080
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Firestore (Native mode)
resource "google_firestore_database" "default" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}
