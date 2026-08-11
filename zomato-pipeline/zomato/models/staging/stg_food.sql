-- Clean and standardize food dimension
select 
    f_id as FOOD_ID,
    item as FOOD_NAME,
    initcap(veg_or_non_veg) as VEG_OR_NON_VEG
from {{ source('raw', 'food') }}
where f_id is not null
