USE WAREHOUSE WEATHER_WH;
USE DATABASE WEATHER;
USE SCHEMA RAW;

CREATE OR REPLACE TABLE RAW_WEATHER_REPORTS (
    LOADED_AT        TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    CITY_NAME        VARCHAR(100),
    RAW_PAYLOAD      VARIANT
);

select * from  RAW_WEATHER_REPORTS;

select * from weather.mart.date_wise_observation;

select * from weather.mart.fct_weather_observations;


