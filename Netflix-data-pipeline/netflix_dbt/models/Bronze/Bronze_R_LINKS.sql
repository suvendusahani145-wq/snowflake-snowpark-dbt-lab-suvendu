{{config(materialized = 'Table', schema= 'Bronze')}}

select cast(movieid as number) as movieid,
       IMDBID,
       TMDBID
    from {{source('RAW','R_LINKS')}}