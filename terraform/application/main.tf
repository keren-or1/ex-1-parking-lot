provider "google" {
  project = var.project_id
  region  = var.region
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

  traffic {
    percent         = 100
    latest_revision = true
  }
}
