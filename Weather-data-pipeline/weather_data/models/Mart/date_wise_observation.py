import snowflake.snowpark.functions as F
from snowflake.snowpark.functions import udf,col
from snowflake.snowpark.types import FloatType
from snowflake.snowpark.window import Window

def model(dbt, session):
    dbt.config(
              materialized="table",
              schema= "Mart",
              python_version ="3.10"
              )
              
    fct_dbt= dbt.ref("fct_weather_observations")
    
    window_spec = Window.partition_by("CITY_ID").order_by(col("OBSERVATION_DT_IST")).rows_between(-2, Window.CURRENT_ROW)
    
    window_city_overall= Window.partition_by(col("CITY_ID"))
    
    window_df= fct_dbt.with_column("date_wise_observation",F.row_number().over(window_spec))
    window_upd_df= fct_dbt.with_column("city_average",F.avg("TEMP_CELSIUS").over(window_city_overall))
    
    return window_upd_df
    
    