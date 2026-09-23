select
    m.movieid,
    m.movie_name,
    gt.tag_name,
    gs.relevance
from {{ref('stg_R_MOVIES')}} m
join {{ref('stg_r_genome_scores')}} gs
    on m.movieid = gs.movieid
join {{ref('stg_r_genome_tags')}} gt
    on gs.tagid = gt.tagid