{{ config(
    materialized='table',
    schema='MART'
) }}

select age_group,count(distinct order_id)  as total_orders,sum(sales_amount) as total_sales_amount
from {{ ref('fct_customer_data') }}
group by age_group