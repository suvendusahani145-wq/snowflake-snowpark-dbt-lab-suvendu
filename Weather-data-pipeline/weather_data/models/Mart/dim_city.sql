{{ config(
         materialized= 'table',schema = 'Mart'
 )}}

-- Select rows from a Table

SELECT DISTINCT city_id,
       city_name,
       sys_country as country,
       coord_lat as lat,
       coord_lon as lon
       from {{ ref('stage_WEATHER_REPORTS') }}
