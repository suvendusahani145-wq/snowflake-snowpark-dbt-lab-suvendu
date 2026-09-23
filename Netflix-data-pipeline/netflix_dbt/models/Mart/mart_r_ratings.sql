select
    RATING_YEAR,
    RATING_MONTH,
    count(*) as TOTAL_RATINGS,
    avg(rating) as AVG_RATING
    FROM {{ref('stg_R_RATINGS')}}
    group by RATING_YEAR,RATING_MONTH