variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
}

variable "image_url" {
  description = "The full URL of the container image to deploy"
  type        = string
}
