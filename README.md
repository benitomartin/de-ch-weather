# Siwss Air Quality Index

<p align="center">
<img align="center" src="/images/airquality.png" height="500">
</p>

This project has been developed as part of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) course provided by [DataTalks.Club](https://datatalks.club/). The data used have been extracted from the [Google Air Quality API](https://developers.google.com/maps/documentation/air-quality).

Below you can find some instructions to understand the project content. Feel free to clone this repo :wink:

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
* CICD: **dbt**

## Project Structure

The project has been structured with the following folders and files:

* `mage:` workflow orchestration pipeline
* `dbt:` data transformation and CI/CD pipeline using dbt
* `looker:` reports from looker studio
* `terraform:` IaC stream-based pipeline infrastructure in GCP using Terraform
* `requirements.txt:` project requirements
* `images:` printouts of results


## Project Description

The dataset was obtained from [Google Air Quality API](https://developers.google.com/maps/documentation/air-quality) and contains various columns with air quality data. To prepare the data some preprocessing steps were conducted. The following actions were performed using **Mage** to get a clean dataset. This [Medium] (https://medium.com/towards-data-science/a-python-tool-for-fetching-air-pollution-data-from-google-maps-air-quality-apis-7cf58a7c63cb) article was taken as reference to understand the API so a big shotout to [Robert Martin-Short](https://github.com/rmartinshort)

* Extract the relevant pollutants and air quality index (AQI) from the API
* Create the columns with the selected cities, latitude and longitude
* Remove rows with NaN
* Remove duplicates
* Create a new column with the country name

Afterwards, the final clean data are ingested to a GCP Bucket and Big Query. Finally, transformations are perfomed using **dbt** (see [dbt](./dbt) folder) to get the production ready data for dashboarding wsing **Looker**.



<h3 align="center"><i>Mage Data Ingestion</i></h3>
&nbsp;

The following picture shows two pipelines used to send the data to the google cloud bucket. It can be sent either directly to the bucket or to a partitioned folder inside the bucket containing the year/month/day structure. The last one is the approach taken so that the file can be updated on a daily basis and the data from prevous days are kept. Finally the data are sent from the bucket to BigQuery.

<p>
    <img src="/images/weather_to_gcs_parquet.png"/>
</p>

<p align="center">
    <img src="/images/gcs_to_bq.png"/>
</p>

<h3 align="center"><i>dbt Data Ingestion</i></h3>
&nbsp;

Once the data are in BigQuery a complete transformation step is performed using **dbt** in order to have the final clean dataset again in BigQuery. There are 4 dataset generated with dbt, two staging and two production, each having the air quality data from all cities and from one city, that can be changed in dbt accordingly. The dataset called `prod_all_cities` is the one taken for the dashboard visualization in Looker.

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

<p align="center">
    <img src="/images/aqitoday.png"/>
</p>
