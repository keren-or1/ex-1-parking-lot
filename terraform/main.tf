provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  name     = "parking-repo"
  format   = "DOCKER"
  location = var.region
}

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

  traffics {
    percent         = 100
    latest_revision = true
  }
}

resource "google_firestore_database" "default" {
  name   = "(default)"
  region = var.region
  type   = "NATIVE"
}
