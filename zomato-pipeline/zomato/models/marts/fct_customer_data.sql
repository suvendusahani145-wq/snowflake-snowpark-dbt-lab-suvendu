{{ config(materialized='incremental', 
          unique_key='order_id', 
          incremental_strategy='merge', 
          on_schema_change='append_new_columns',
          schema= 'MART' ) }}

with customer_data as(
select 
order_id,
u.customer_id,
customer_name,
age,
gender,
sales_amount,
MARITAL_STATUS,
income_band,
r.Restaurant_ID,
r.Restaurant_Name,
r.CITY,
CASE WHEN age < 25 then 'Gen Z'
     WHEN age < 40 then 'Millennial'
     WHEN age < 55 then 'Elders'
     WHEN age is null then 'Unknown'
     ELSE 'Boomer' 
     END AS AGE_GROUP from 
{{ ref('stg_orders') }} o inner join {{ ref('stg_users') }} u
on(o.customer_id=u.customer_id)
inner join {{ ref('stg_restaurants') }} r
on(o.restaurant_id=r.restaurant_id)
)select * from customer_data

