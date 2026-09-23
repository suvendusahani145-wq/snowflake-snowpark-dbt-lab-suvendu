{{config(materialized = 'Table', schema= 'Bronze')}}
select 
      cast(movieid as number) as movieid,
      TAGID,
      RELEVANCE
      from {{ source('RAW','R_GENOME_SCORES') }}