{{ config(
    materialized='table'
    )
}}


with weather_ch as

(
    select * 
    from {{ ref('stg_one_city') }}
)

-- Select Relevant Columns
select
    -- City
    weather_ch.city,
    weather_ch.lat,
    weather_ch.lon,

    -- Air Quality
    weather_ch.category,
    weather_ch.warnings,
    weather_ch.aqi,
    weather_ch.co_concentration,
    weather_ch.no2_concentration,
    weather_ch.o3_concentration,
    weather_ch.pm10_concentration,
    weather_ch.pm25_concentration,
    weather_ch.so2_concentration,

    -- Time
    weather_ch.day,
    weather_ch.time

from weather_ch
where city = "Zurich"
