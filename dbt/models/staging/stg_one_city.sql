{{ config(
    materialized='view'
    )
}}


with weather_ch as

(
    select * 
    from {{ source('staging', 'cities') }}
)

-- Select Relevant Columns
select
    -- City
    city,
    lat,
    lon,

    -- Air Quality
    category,
    {{ get_warnings('category') }} as warnings,
    aqi,
    co_concentration,
    no2_concentration,
    o3_concentration,
    pm10_concentration,
    pm25_concentration,
    so2_concentration,

    -- Time
    cast(day as timestamp) as day,
    time

from weather_ch
where city = "Zurich"

-- dbt build --select <model_name> --vars {'is_test_run: false'}
{% if var('is_test_run', default=true) %}

    -- Limit the result to 100 rows
    limit 100

{% endif %}