select 
    city,
    count(*) as total_orders,
    sum(case when is_delivered = true then 1 else 0 end) as total_order_delivered,
    sum(case when is_delivered = false then 1 else 0 end) as total_order_cancelled
from {{ ref('fct_orders') }}
group by city
order by total_orders desc
