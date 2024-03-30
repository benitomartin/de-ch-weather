# dbt Data Transformation

This folder contains all files generated in dbt cloud. I recommend emptying the folder and initialize the project in dbt. While connecting the repo in dbt, make sure you add the generated deploy key in dbt to your repo under settings, deploy key (allow write access).

## Set Up:

- Create as Dataset in BigQuery and make sure it is created using the same region as your bucket.

- While creating the project in dbt, use the same dataset name and connect it to the subfolder `dbt` of the repo.

- Initialize the project in dbt using a new branch.

Afterwards copy/create the following files from the repo:

- `dbt_project.yml`: give a project name and put the same name under models in the same file
- `Macros` folder:
  - `get_warnings.sql`: contains a macro to create a new column with weather warnings
- `Models` folder:
  - `Core` folder: contains the production model
    - `schema.yml`: model schema including tests
    - `prod_one_city.sql`: model to get the weather from an specific city (Change the name of the city accordingly)
    - `prod_all_cities.sql`: model to get the weather from all cities
  - `Staging` folder: contains the staging model
    - `schema.yml`: model schema including tests
    - `stg_one_city.sql`: model to get the weather from an specific city (Change the name of the city accordingly)
    - `stg_all_cities.sql`: model to get the weather from all cities

- `packages.yml`: contains dbt-labs/dbt_utils and dbt-labs/codegen

Now in the dbt terminal run the following to install the `packages.yml`:

    dbt deps

## Development Environment

By default, dbt creates a Development environment. Therefore, here it is shown how to run the files under models/staging. For production go to the next chapter below.

- Run a model selecting a model file under models/staging. The generated table shall be visible in BigQuery:

        dbt run --select stg_all_cities

- By default the generated table will have all rows. But you can uncomment the last five lines of code to get a desired amount of rows. If you do so, you can run the following code to get all rows with the uncommented lines:

        dbt run --models stg_all_cities --vars '{"is_test_run": false}'

- To run the tests included in the `schema.yml` file run:

        dbt test --select stg_all_cities

- To run the file and the tests together run:

        dbt run --select stg_all_cities

## Production Environment

Create a new environment in dbt cloud called Production. In the new Production environment, create a new job and add commands or triggers. As a first approach I recommend as commands:

- dbt run
- dbt run --vars '{"is_test_run": false}'
- dbt test

Or you can just simply add `dbt build` as a single command.

If you want to generate documentation, while creating the job click on `Generate docs on run`. This will generate a new Documentation. You can access the documentation under account settings, select project and under artifacts add the generated documentation, so you have a link to the documentation.
