select
menu_id,
try_to_number(R_ID) as restaurant_id,
f_id as food_id,
cuisine,
price
from
{{source('raw','menu')}} where menu_id is not null and try_to_decimal(price,10,2) > 0