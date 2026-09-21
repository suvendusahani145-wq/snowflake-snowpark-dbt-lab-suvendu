from snowflake.snowpark import functions as F
from snowflake.snowpark.functions import udf,col
from snowflake.snowpark.types import FloatType
from snowflake.snowpark.window import Window

def model(dbt, session):

    dbt.config(materialized= 'table',
               schema= 'Mart',
               python_version='3.10'
               )
        
    customer_data_dbt= dbt.ref('fct_customer_data')
        
    review_dbt= dbt.ref("stg_reviews")
    menu_dbt= dbt.ref("stg_menu")
        
    customer_data_result=  customer_data_dbt.group_by("RESTAURANT_ID").agg(F.count("order_id").alias("TOTAL_ORDERS"),F.sum("SALES_AMOUNT").alias("TOTAL_SALES"),F.count_distinct("customer_id").alias("Total_Customer_reach")) 
        
    review_result= review_dbt.group_by("RESTAURANT_ID").agg(F.avg("RATING").alias("AVG_RATING"),
                                                                F.count("REVIEW_ID").alias("NUMBER_OF_RATING"))
                                                                
    menu_diversity =   menu_dbt.group_by("RESTAURANT_ID").agg(F.count_distinct("FOOD_ID").alias("Menu_count"))
    
    restaurant_dim = dbt.ref("dim_restaurants")
        
    restaurant_score_df= customer_data_result.join(review_result,on="RESTAURANT_ID",how="left").join(menu_diversity,on="RESTAURANT_ID",how="left").join(restaurant_dim,on="RESTAURANT_ID",how="left")
        
    order_Window= Window.order_by(F.col("TOTAL_ORDERS"))
    restaurant_score_df= restaurant_score_df.with_column("order_score", F.percent_rank().over(order_Window))
        
    sales_Window= Window.order_by(F.col("TOTAL_SALES"))
    restaurant_score_df= restaurant_score_df.with_column("sales_score",F.percent_rank().over(sales_Window))
        
    ratings_Window= Window.order_by(F.col("NUMBER_OF_RATING"))
    restaurant_score_df= restaurant_score_df.with_column("ratings_score",F.percent_rank().over(ratings_Window))
    
    ratings_AVG= Window.order_by(F.col("AVG_RATING"))
    restaurant_score_df= restaurant_score_df.with_column("avg_ratings_score",F.percent_rank().over(ratings_AVG))
        
    customer_Window= Window.order_by(F.col("Total_Customer_reach"))
    restaurant_score_df= restaurant_score_df.with_column("customer_score",F.percent_rank().over(customer_Window))
        
    menu_Window= Window.order_by(F.col("Menu_count"))
    restaurant_score_df= restaurant_score_df.with_column("menu_score",F.percent_rank().over(menu_Window))
        
    restaurant_score_df= restaurant_score_df.with_column("restaurant_score",F.col("order_score")*0.25+F.col("sales_score")*0.25+F.col("ratings_score")*0.1+F.col("avg_ratings_score")*0.15+F.col("customer_score")*0.15+F.col("menu_score")*0.1)
        
    restaurant_score_df= restaurant_score_df.with_column("RESTAURANT_TIER",F.when(F.col("RESTAURANT_SCORE") >= 0.90 ,"PLATINUM")
                                                                                .when(F.col("RESTAURANT_SCORE") >= 0.75 ,"GOLD")
                                                                                .when(F.col("RESTAURANT_SCORE") >= 0.50 ,"SILVER")
                                                                                .otherwise("BRONZE"))
    
    
    RESTAURANT_RANK_Window= Window.order_by(F.col("RESTAURANT_SCORE").desc())
    restaurant_score_df= restaurant_score_df.with_column("RESTAURANT_RANK",F.rank().over(RESTAURANT_RANK_Window))
        
    return restaurant_score_df


    
        
    
        