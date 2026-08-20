select
     TAGID,
     TAG
     from 
     {{ ref('Bronze_r_genome_tags') }}