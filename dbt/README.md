# dbt Data Transformation

This folder contains all files generated in dbt cloud. I recommend emptying the folder and initialize the project in dbt. While connecting the repo in dbt, make sure you add the generated deploy key in dbt to your repo under settings, deploy key (allow write access).

Set up:

- Create as Dataset in BigQuery and make sure it is created using the same region as your bucket.

- While creating the project in dbt, use the same dataset name and connect it to the subfolder `dbt` of the repo.

- Initialize the project in dbt using a new branch. Otherwise, you will only have read-only access to your files and can't be modified.

Afterwards copy/create the following files from the repo:

- `dbt_project.yml`: give a project name and put the same name under models in the same file
- `Macros` folder:
  - `get_hotel_rating_description.sql`: contains a macro to create a new column with hotel rating
- `Models` folder:
  - `Core` folder: contains the production model
    - `schema.yml`: model schema including tests
    - `prod_hotel_reviews.sql`: model to get all reviews from all countries
    - `prod_hotel_reviews_country.sql`: model to get all reviews from one country. You must select a country name inside the file
  - `Staging` folder: contains the staging model
    - `schema.yml`: model schema including tests
    - `stg_hotel_reviews.sql`: model to get all reviews from all countries
    - `stg_hotel_reviews_country.sql`: model to get all reviews from one country. You must select a country name inside the file

- `packages.yml`: contains dbt-labs/dbt_utils

Now in the dbt terminal run the following to install the `packages.yml`:

    dbt deps

## Development Environment

By default, dbt creates a Development environment. Therefore, here it is shown how to run the files under models/staging. For production go to the next chapter below.

- Run a model selecting a model file under models/staging. The generated table shall be visible in BigQuery:

        dbt run --select stg_hotel_reviews

- By default the generated table will have 100 rows. To get the complete table run:

        dbt run --models stg_hotel_reviews --vars '{"is_test_run": false}'

- To run the tests included in the `schema.yml` file run:

        dbt test --select stg_hotel_reviews

- To run the file and the tests together run:

        dbt run --select stg_hotel_reviews

## Production Environment

Create a new environment in dbt cloud called Production and use as dataset a different one than the one used in staging. Create this dataset in advance in BigQuery using the same region as your bucket. This will allow you to separate the development models from the productions models.

In the new Production environment, create a new job and add commands or triggers. As a first approach I recommend as commands:

- dbt run
- dbt run --vars '{"is_test_run": false}'
- dbt test

If you want to generate documentation, while creating the job click on `Generate docs on run. This will generate a new Documentation. You can access the documentation under account settings, select project and under artifacts add the generated documentation, so you have a link to the documentation.
