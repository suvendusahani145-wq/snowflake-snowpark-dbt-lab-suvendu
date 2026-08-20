select
    MOVIEID,
    title,
    movie_name,
    release_year,
    genres,
    regexp_count(genres,'[|]') + 1 as no_of_genres
from {{ ref('stg_R_MOVIES') }}