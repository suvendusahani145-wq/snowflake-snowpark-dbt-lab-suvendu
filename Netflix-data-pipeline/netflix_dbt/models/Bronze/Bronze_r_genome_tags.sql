select
     TAGID,
     TAG
     from 
     {{ source('Bronze','r_genome_tags') }}