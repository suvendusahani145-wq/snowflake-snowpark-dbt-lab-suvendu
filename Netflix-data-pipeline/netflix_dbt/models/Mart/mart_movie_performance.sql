select m.movieid,
    m.movie_name,
    avg(r.rating) as avg_rating,
    count(r.rating) as rating_count,
    count(t.tag) as tag_count
from {{ref('stg_R_MOVIES')}} m
left join {{ref('stg_R_RATINGS')}} r
    on m.movieid = r.movieid
left join {{ref('stg_R_TAGS')}} t
    on m.movieid = t.movieid
group by
    m.movieid,m.movie_name