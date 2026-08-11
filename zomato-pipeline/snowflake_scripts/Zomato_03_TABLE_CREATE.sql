USE ROLE ACCOUNTADMIN;
USE DATABASE ZOMATO;
USE SCHEMA RAW;

CREATE OR REPLACE TABLE RAW.RESTAURANTS
(_Idx NUMBER AUTOINCREMENT START = 1 INCREMENT = 1,
 id STRING PRIMARY KEY,
 name STRING,
 city string,
 rating STRING,
 rating_count string,
 cost string,
 cusine string,
 lic_no string,
 link string,
 address string,
 menu string);


CREATE OR REPLACE TABLE ZOMATO.RAW.FOOD (
    food_key NUMBER AUTOINCREMENT START = 1 INCREMENT = 1,  -- auto-generated key
    f_id STRING PRIMARY KEY,                                       -- fd0, fd1, etc.
    item STRING,                                            -- food item name
    veg_or_non_veg STRING                                   -- Veg / Non-veg
);


CREATE OR REPLACE TABLE ZOMATO.RAW.MENU (
   M_KEY NUMBER AUTOINCREMENT START = 1 INCREMENT = 1,  -- auto-generated key
   MENU_ID STRING,
   R_ID STRING,
   F_ID STRING,
   CUISINE STRING,
   PRICE NUMBER(10,2),                                  -- store price as numeric
   CONSTRAINT fk_menu_rest FOREIGN KEY (R_ID) REFERENCES ZOMATO.RAW.RESTAURANTS(ID),
   CONSTRAINT fk_menu_food FOREIGN KEY (F_ID) REFERENCES ZOMATO.RAW.FOOD(F_ID)
);
CREATE OR REPLACE TABLE ZOMATO.RAW.USERS (
    user_key NUMBER AUTOINCREMENT START = 1 INCREMENT = 1,  -- internal unique key
    user_id STRING,                                         -- external business ID
    name STRING,
    email STRING,
    password STRING,
    age NUMBER,
    gender STRING,
    marital_status STRING,
    occupation STRING,
    monthly_income STRING,
    educational_qualifications STRING,
    family_size NUMBER,
    CONSTRAINT pk_users PRIMARY KEY (user_ID)
);



CREATE OR REPLACE TABLE ZOMATO.RAW.ORDERS (
    order_id STRING,                                        -- business/order ID
    order_timestamp TIMESTAMP,                              -- full timestamp
    order_date DATE,                                        -- date only
    user_id STRING,                                         -- customer/user ID
    r_id STRING,                                            -- restaurant ID
    restaurant_city STRING,                                 -- city/location
    cuisine STRING,                                         -- cuisine types
    items_count NUMBER,                                     -- number of items
    sales_qty NUMBER,                                       -- total quantity
    subtotal NUMBER(10,2),                                  -- subtotal before discounts
    discount NUMBER(10,2),                                  -- discount amount
    delivery_fee NUMBER(10,2),                              -- delivery charge
    gst NUMBER(10,2),                                       -- tax amount
    sales_amount NUMBER(10,2),                              -- total payable
    currency STRING,                                        -- e.g., INR
    payment_method STRING,                                  -- UPI, COD, Card, Wallet
    order_status STRING,                                    -- Delivered, Cancelled, etc.
    customer_rating NUMBER(2,1),                            -- rating (e.g., 4.5)
    delivery_time_min NUMBER(5,2),                          -- delivery duration in minutes
    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_rest FOREIGN KEY (r_id) REFERENCES ZOMATO.RAW.RESTAURANTS(ID),
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES ZOMATO.RAW.USERS(user_id)
);





CREATE OR REPLACE TABLE ZOMATO.RAW.ORDER_ITEMS (
    order_item_id NUMBER AUTOINCREMENT START = 1 INCREMENT = 1,  -- auto-generated key
    order_id STRING,                                             -- order identifier
    r_id STRING,                                                 -- restaurant ID
    f_id STRING,                                                 -- food ID
    price NUMBER(10,2),                                          -- item price
    quantity NUMBER,                                             -- quantity ordered
    line_amount NUMBER(10,2),                                    -- total amount per line
    CONSTRAINT pk_order_items PRIMARY KEY (order_id),
    CONSTRAINT fk_order_rest FOREIGN KEY (r_id) REFERENCES ZOMATO.RAW.RESTAURANTS(ID),
    CONSTRAINT fk_order_food FOREIGN KEY (f_id) REFERENCES ZOMATO.RAW.FOOD(F_ID)
);


CREATE OR REPLACE TABLE ZOMATO.RAW.REVIEWS (
    review_id NUMBER AUTOINCREMENT START = 1 INCREMENT = 1,  -- auto-generated key
    order_id STRING,                                         -- links to ORDERS table
    user_id STRING,                                          -- links to USERS table
    restaurant_id STRING,                                    -- links to RESTAURANTS table
    rating NUMBER(2,1),                                      -- rating value (e.g., 4.5)
    comment STRING,                                          -- review text
    review_date DATE,                                        -- date of review
    CONSTRAINT pk_reviews PRIMARY KEY (review_id),
    CONSTRAINT fk_reviews_order FOREIGN KEY (order_id) REFERENCES ZOMATO.RAW.ORDERS(order_id),
    CONSTRAINT fk_reviews_rest FOREIGN KEY (restaurant_id) REFERENCES ZOMATO.RAW.RESTAURANTS(ID),
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES ZOMATO.RAW.USERS(user_id)
);




