-- parse the messy dimension (-- →null, 50+ ratings→50, ₹ 200→200, city after last comma):

select id as RESTAURANT_ID,
       name as RESTAURANT_NAME,
          
        coalesce(REGEXP_SUBSTR(city,'[^,]+$'), city) as CITY,
        try_to_decimal(nullif(rating, '--'), 3, 1) as rating,
        try_to_number(REGEXP_SUBSTR(RATING_COUNT, '[0-9]+')) as RATING_COUNT,
        try_to_number(REGEXP_SUBSTR(COST, '[0-9]+')) as COST_FOR_TWO,
        cusine, 
        LIC_NO AS LICENSE_NUMBER
        FROM {{ source('raw', 'restaurants') }} where try_to_number(id) is not null


       
          