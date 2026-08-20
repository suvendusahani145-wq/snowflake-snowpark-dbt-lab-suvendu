select MOVIEID,
       title,
       regexp_replace(title,'[0-9()]+','') movie_name,
       regexp_substr(title,'[0-9]+') release_year,
       genres
from {{ref('Bronze_R_MOVIES')}}