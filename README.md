# Swiss Air Quality Index

<p align="center">
<img align="center" src="/images/aqitoday.png">
</p>

This project has been developed as part of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) course provided by [DataTalks.Club](https://datatalks.club/). The data used has been extracted from the [Google Air Quality API](https://developers.google.com/maps/documentation/air-quality).

Below, you can find the project descrition to understand the content and setup instructions. Feel free to ⭐ and clone this repo 😉

## Tech Stack

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B.svg?style=for-the-badge&logo=dbt&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Looker Studio](https://img.shields.io/badge/Looker-4285F4.svg?style=for-the-badge&logo=Looker&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)


* Data Analysis & Exploration: **SQL/Python**
* Cloud: **Google Cloud Platform**
  * Data Lake - **Google Cloud Storage**
  * Data Warehouse: **BigQuery**
* Infrastructure as Code (IaC): **Terraform**
* Data ingestion (Batch/Workflow Orchestration): **Mage**
* Data Transformation: **dbt**
* Data Visualization: **Looker Studio**
* CI/CD: **dbt**

## Project Structure

The project has been structured with the following folders and files:

* `mage:` Workflow orchestration pipeline
* `dbt:` Data transformation and CI/CD pipeline
* `looker:` Report from Looker Studio
* `terraform:` IaC stream-based pipeline infrastructure in GCP using Terraform
* `requirements.txt:` Project requirements
* `images:` Printouts of results


## Project Description

The dataset was obtained from [Google Air Quality API](https://developers.google.com/maps/documentation/air-quality) and contains various columns with air quality data for a specific list of Swiss cities. To prepare the data some preprocessing steps were conducted. The following actions were performed using **Mage** to get a clean dataset. This [Medium](https://medium.com/towards-data-science/a-python-tool-for-fetching-air-pollution-data-from-google-maps-air-quality-apis-7cf58a7c63cb) article was used as reference to understand the API and extract the data. A big shotout to [Robert Martin-Short](https://github.com/rmartinshort) for the tutorial.

* Extract the relevant pollutants and air quality index (AQI) from the API
* Create the columns with the selected cities, latitude, and longitude
* Remove rows with NaN values
* Remove duplicates

Afterward, the final clean data are ingested to a GCP Bucket and Big Query. Finally, transformations are perfomed using **dbt** (see [dbt](./dbt) folder) to get the production-ready data for dashboarding using **Looker**.



<h3 align="center"><i>Mage Data Ingestion</i></h3>
&nbsp;

The following picture shows two pipelines used to send the data to the Google Cloud bucket. It can be sent either directly to the bucket or to a partitioned folder inside the bucket containing the year/month/day structure. The latter approach is taken so that the file can be updated on a daily basis and the data from previous days are kept. Finally, the data is sent from the bucket to BigQuery.

<p>
    <img src="/images/weather_to_gcs_parquet.png"/>
</p>

<p align="center">
    <img src="/images/gcs_to_bq.png"/>
</p>

<h3 align="center"><i>dbt Data Transformation</i></h3>
&nbsp;

Once the data is in BigQuery, a complete transformation step is performed using **dbt** to have the final clean dataset again in BigQuery. Four datasets are generated with dbt, two staging, and two production, each having the air quality data from all cities and from one city, which can be changed in dbt accordingly. The dataset called `prod_all_cities` is the one taken for the dashboard visualization in Looker. For the deployment in Github a CI/CD Check was run in dbt with the command `dbt build --select state:modified+`

<p align="center">
    <img src="/images/dbt.png"/>
</p>

## Visualization


<p align="center">
    <img src="/images/air7days.png"/>
</p>

<p align="center">
    <img src="/images/aqi7days.png"/>
</p>

## CI/CD

Finally, to streamline the development process, a fully automated **Build** and **CI/CD** pipeline was created using dbt:

<h3 align="center"><i>dbt Build</i></h3>
&nbsp;

<p align="center">
<img src="/images/dbt2.png" height="300">
</p>

<h3 align="center"><i>dbt CI/CD</i></h3>
&nbsp;

<p>
    <img src="/images/dbt.png"/>
</p>


## Project Set Up

The Python version used for this project is Python 3.10.

1. Clone the repo (or download it as zip):

   ```bash
   git clone https://github.com/benitomartin/de-ch-weather.git
   ```

2. Create the virtual environment named `main-env` using Conda with Python version 3.10:

   ```bash
   conda create -n main-env python=3.10
   conda activate main-env
   ```

3. Execute the `requirements.txt` script and install the project dependencies:

    ```bash
    pip install -r requirements.txt

    ```

4. Install terraform:

   ```bash
   conda install -c conda-forge terraform
    ```

Each project folder contains a **README.md** file with instructions about how to run the code. I highly recommend creating a virtual environment for each one. Additionally, please note that a **GCP Account**, credentials, and proper **IAM** roles are necessary for the scripts to function correctly. The following IAM Roles have been used for this project:

* BigQuery Data Editor
* BigQuery Job User
* BigQuery User
* BigQuery Admin
* Storage Admin
* Compute Admin

## Evaluation Criteria

The following criteria for the evaluation have been fulfilled:

- :white_check_mark: **Problem description**: The project is well described and it's clear and understandable
- :white_check_mark: **Cloud**: The project is developed on the cloud (Google) and IaC tools (Terraform) are used for provisioning the infrastructure
- :white_check_mark: **Data Ingestion**: Fully deployed workflow orchestration using Mage
- :white_check_mark: **Data warehouse**: Tables are created in BigQuery
- :white_check_mark: **Transformations**: Tables are transformed using dbt
- :white_check_mark: **Dashboard**: 3 Pages with 6 visualizations using Looker
- :white_check_mark: **Reproducibility**: Instructions are clear, it's easy to run the code, and it works. 
