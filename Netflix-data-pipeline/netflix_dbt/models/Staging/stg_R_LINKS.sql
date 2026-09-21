select
    movie_id,
    imdb_id,
    tmdb_id,
    concat('https://www.imdb.com/title/tt', imdb_id) as imdb_url,
    case
        when tmdb_id is null
        then 'NOT_AVAILABLE'
        else 'AVAILABLE'
    end as tmdb_status
from {{ ref('Bronze_R_LINKS') }}
