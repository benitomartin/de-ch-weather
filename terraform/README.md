# IaC Terraform

The code here is the IaC for setting up in GCP an infrastructure using Terraform.

The `variables.tf` file contains the following variable that must be defined to set up the infrastructure:

- credentials: "your-json-service-account-credentials"
- project = "your-project-id""
- gcs_bucket_name = "your-bucket-name"
- bq_dataset_name = "your-bq-dataset"
- location = "your-bucket-location"
- region = "your-bucket-region"
- gcs_storage_class = "your-storage-class"

Then follow the next steps:

- Initialize Terraform:

    ```bash
    terraform init
    ```

- Plan and apply Terraform:

    ```bash
    terraform plan 
    ```

    ```bash
    terraform apply 
    ```

This will create the required bucket and bq dataset.
