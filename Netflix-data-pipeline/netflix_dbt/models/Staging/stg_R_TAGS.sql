select
    user_id,
    movie_id,
    tag,
    tag_timestamp,
    cast(tag_timestamp as date) as tag_date,
    extract(year from tag_timestamp) as tag_year,
    extract(month from tag_timestamp) as tag_month,
    extract(day from tag_timestamp) as tag_day,
    
    case
        when tag is null then 'INVALID'
        else 'VALID'
    end as tag_status
from {{ ref('Bronze_R_TAGS') }}