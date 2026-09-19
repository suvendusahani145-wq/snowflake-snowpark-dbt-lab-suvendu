{{ config(
    materialized='table',
    schema='MART'
) }}

select gender, count(*) as Total_orders
from {{ ref('fct_customer_data') }}
group by gender