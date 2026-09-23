{{config(materialized = 'Table', schema= 'Bronze')}}
select cast(movieid as number) as movieid,
    trim(tag) as tag,
    trim(title) as title, 
    trim(genres) as genres,
    current_timestamp() as load_ts
from {{ source('RAW', 'R_MOVIES') }}