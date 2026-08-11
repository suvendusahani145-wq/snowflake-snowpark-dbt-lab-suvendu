USE ROLE ACCOUNTADMIN;
USE DATABASE ZOMATO;
USE SCHEMA RAW;
USE WAREHOUSE ZOMATO_WH;

list @zomato_stage;



COPY INTO RAW.USERS
FROM @zomato_stage/raw/users/users.csv
FILE_FORMAT = CSV_FMT;


SELECT * FROM  RAW.USERS ;


COPY INTO RAW.RESTAURANTS
FROM @zomato_stage/raw/restaurant/restaurant.csv
FILE_FORMAT = CSV_FMT;

SELECT * FROM  RAW.RESTAURANTS limit 50;

COPY INTO RAW.FOOD
FROM @zomato_stage/raw/food/food.csv
FILE_FORMAT = CSV_FMT;

SELECT * FROM  RAW.food ;

COPY INTO RAW.MENU
FROM @zomato_stage/raw/menu/menu.csv
FILE_FORMAT = CSV_FMT
ON_ERROR=CONTINUE;

SELECT * FROM  RAW.MENU limit 20;

SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'RAW.MENU',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));

SELECT $1, $2, $3
FROM @zomato_stage/raw/menu/ (FILE_FORMAT => CSV_FMT);

LIST @zomato_stage/raw/menu/;

COPY INTO RAW.MENU
FROM @zomato_stage/raw/menu/menu.csv
FILE_FORMAT = CSV_FMT
VALIDATION_MODE = 'RETURN_ERRORS';


SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'RAW.MENU',
    START_TIME => DATEADD('hour', -2, CURRENT_TIMESTAMP())
));

TRUNCATE TABLE RAW.MENU;

SELECT job_id,
       table_name,
       file_name,
       rows_parsed,
       rows_loaded,
       error_count,
       first_error_message,
       last_error_message
FROM TABLE(COPY_HISTORY(
    TABLE_NAME => 'RAW.MENU',
    START_TIME => DATEADD('hour', -2, CURRENT_TIMESTAMP())
));


SELECT COUNT(*) FROM  RAW.orders ;


COPY INTO RAW.ORDER_ITEMS
FROM @zomato_stage/raw/order_items/order_items.csv
FILE_FORMAT = CSV_FMt;


select count(*) from raw.order_items;



COPY INTO RAW.REVIEWS
FROM @zomato_stage/raw/reviews/reviews.csv
FILE_FORMAT = CSV_FMt;


select * from raw.reviews;








COPY INTO RAW.ORDERS
FROM @zomato_stage/raw/orders/orders.csv
FILE_FORMAT = CSV_FMT
ON_ERROR=CONTINUE;


select * from  RAW.ORDERS;
