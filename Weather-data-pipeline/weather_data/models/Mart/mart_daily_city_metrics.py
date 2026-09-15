import snowflake.snowpark.functions as F
from snowflake.snowpark.functions import udf,col
from snowflake.snowpark.types import FloatType
from snowflake.snowpark.window import Window


def model(dbt,session):
    
    dbt.config(
        materialized="table",
        schema="Mart",
        python_version="3.10"
    )
    
    fct_observation = dbt.ref("fct_weather_observations")
    
    fct_observation = fct_observation.with_column("OBSERVATION_DAY", F.date_trunc("DAY", col("OBSERVATION_DT_IST")))
    
    agg_df = fct_observation.group_by("OBSERVATION_DAY").agg(
        F.min(F.col("TEMP_CELSIUS")).alias("min_temp"),
        F.max(F.col("TEMP_CELSIUS")).alias("max_temp"),
        F.avg(F.col("TEMP_CELSIUS")).alias("avg_temp"),
        F.sum(F.col("TEMP_CELSIUS")).alias("Total_temp")
    )
    
    return agg_df