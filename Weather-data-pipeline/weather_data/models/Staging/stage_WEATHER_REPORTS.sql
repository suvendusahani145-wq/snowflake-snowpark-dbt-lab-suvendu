{{config(
         materialized= 'incremental',
         unique_key= ['city_name','weather_dt'],
         incremental_strategy= 'merge'
)}}

select RAW_PAYLOAD_HASH,
       base,
       clouds_all,
       cod,
       coord_lat,
       coord_lon,
       weather_dt,
       city_id,
       round(main_feels_like-273.15, 2) as main_feels_like_celsius,
       main_grnd_level,
       main_humidity,
       main_pressure,
       main_sea_level,
       round(main_temp - 273.15, 2) as main_temp_celsius,
       round(main_temp_max - 273.15, 2) as main_temp_max_celsius,
       round(main_temp_min - 273.15, 2) as main_temp_min_celsius,
       city_name,
       sys_country,
       sys_id,
       to_timestamp_ntz(sys_sunrise) as sunrise_time,
       to_timestamp_ntz(sys_sunset) as sunset_time,
       sys_type,
       timezone,
       visibility,
       weather_description,
       weather_icon,
       weather_id,
       weather_main,
       wind_deg,
       wind_gust,
       wind_speed
       from {{ ref('Bronze_RAW_WEATHER_REPORTS') }}  

       {% if is_incremental() %}
       where weather_dt > (select max(weather_dt) from {{ this }})
       {% endif %}