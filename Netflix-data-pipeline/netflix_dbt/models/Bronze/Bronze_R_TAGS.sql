{{config(materialized = 'Table', schema= 'Bronze')}}

select cast(userid as NUMBER) as user_id,
    cast(movieid as number) as movie_id,
    trim(tag) as tag,
    TAG_TIMESTAMP,
    current_timestamp() as load_ts
from {{ source('RAW','R_TAGS') }}