select RESTAURANT_ID,
       RESTAURANT_NAME,
       CITY,
       rating,
       RATING_COUNT,
       COST_FOR_TWO,
       cusine, 
       LICENSE_NUMBER
       FROM {{ ref('stg_restaurants')}}