{{config(materialized = 'Table', schema= 'Bronze')}}
select
     cast(TAGID as NUMBER) as TAGID,
     trim(tag) as tag
     from 
     {{ source('RAW','r_genome_tags') }}