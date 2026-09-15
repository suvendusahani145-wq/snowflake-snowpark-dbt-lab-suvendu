{{ config(
    materialized = 'incremental',
    unique_key = 'observation_id',
    incremental_strategy = 'merge',
    schema = 'Mart'
) }}

with source_data as (
    select 
        city_id || '_' || weather_dt as observation_id,
        city_id,
        weather_dt,
        convert_timezone('UTC', weather_dt) as observation_dt_utc,
        convert_timezone('UTC', 'Asia/Kolkata', weather_dt) as observation_dt_ist,
        main_feels_like_celsius as feels_like_celsius,
        main_temp_celsius as temp_celsius,
        main_temp_max_celsius as temp_max_celsius,
        main_temp_min_celsius as temp_min_celsius,
        main_humidity as humidity,
        main_pressure as pressure,
        wind_speed as wind_speed,
        wind_deg as wind_direction,
        case 
            when weather_dt between sunrise_time and sunset_time then 'Day' 
            else 'Night' 
        end as day_night_flag
    from {{ ref('stage_WEATHER_REPORTS') }}

    {% if is_incremental() %}
        where weather_dt > (select max(weather_dt) from {{ this }})
    {% endif %}

    qualify row_number() over (partition by city_id, weather_dt order by weather_dt desc) = 1
)

select * from source_data