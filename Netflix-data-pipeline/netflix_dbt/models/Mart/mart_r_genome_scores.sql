select 
      MOVIEID,
      TAGID,
      RELEVANCE,
      from {{ ref('stg_r_genome_scores') }}
      WHERE RELEVEANT_OR_NOT='RELEVANT'