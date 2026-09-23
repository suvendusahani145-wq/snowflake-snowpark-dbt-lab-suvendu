{{config(materialized = 'Table', schema= 'Bronze')}}
select cast(userid as number) as user_id,
    cast(movieid as number) as movieid,
    cast(rating as decimal(2,1)) as rating,
    rating_timestamp,
    current_timestamp() as load_ts
from {{ source('RAW','R_RATINGS') }}