select 
      MOVIEID,
      TAGID,
      RELEVANCE
      from {{ source('Bronze','r_genome_scores') }}