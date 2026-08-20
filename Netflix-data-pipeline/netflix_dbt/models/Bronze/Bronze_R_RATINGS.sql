select
    movieid,
    RATING,
    RATING_TIMESTAMP
from {{ source('Bronze', 'R_RATINGS') }}