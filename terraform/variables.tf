variable "credentials" {
  description = "My Credentials"
  default     = "C:/Users/bmart/.google/credentials/terraform_key.json"

}

variable "project" {
  description = "Your GCP Project ID" # Description for the 'project' variable
  default     = "active-411914"       # Zurich is the default GCP region (you can change it if needed)

}

variable "region" {
  description = "Region for GCP resources. https://cloud.google.com/about/locations"
  default     = "europe-west6" # Zurich is the default GCP region (you can change it if needed)
  type        = string         # Type constraint for the 'region' variable (string)
}

variable "location" {
  description = "Project location: https://cloud.google.com/about/locations"
  default     = "EU" # Zurich is the default GCP region (you can change it if needed)
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset"
  # default     = "example_dataset" # Default BigQuery dataset name is 'hotels_all'
  # default     = "weather_data" # Default BigQuery dataset name is 'hotels_all'
  default     = "weather" # Default BigQuery dataset name is 'hotels_all'

}

variable "gcs_bucket_name" {
  description = "The name of the GC Storage Bucket."
  # default     = "active-411914-terraform-bucket" # Default storage class is 'STANDARD'
  default     = "mage-zoomcamp-ben" # Default storage class is 'STANDARD'

}

variable "gcs_storage_class" {
  description = "Storage class type for your bucket."
  default     = "STANDARD" # Default storage class is 'STANDARD'
}