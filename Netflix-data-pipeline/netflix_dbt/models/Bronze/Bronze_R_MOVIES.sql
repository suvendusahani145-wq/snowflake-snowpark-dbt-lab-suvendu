select
    movieid,
    title,
    genres
from {{ source('Bronze', 'R_MOVIES') }}