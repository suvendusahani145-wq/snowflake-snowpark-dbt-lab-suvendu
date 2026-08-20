select 
      MOVIEID,
      TAGID,
      RELEVANCE,
      CASE WHEN RELEVANCE=0
      THEN
      'NON-RELEVANT'
      ELSE
       'RELVEANT'
      END AS RELEVEANT_OR_NOT
      from {{ ref('Bronze_r_genome_scores') }}