import pandas as pd
import numpy as np
import snowflake.snowpark.functions as F
from snowflake.snowpark.functions import udf
from snowflake.snowpark.types import FloatType


def model(dbt, session):
    dbt.config(
        materialized="table",
        packages=["pandas", "numpy"],
        schema='Mart',
        python_version="3.10"
    )

    fct_df = dbt.ref("fct_weather_observations")

    # Use standard scalar @udf registered with FloatType
    @udf(
        return_type=FloatType(),
        input_types=[FloatType(), FloatType(), FloatType()]
    )
    def index_calculation(v_humidity: float, v_pressure: float, v_temp: float) -> float:
        if v_humidity is None or v_temp is None:
            return None
            
        v_temp_f = (v_temp * 1.8) + 32.0

        if v_temp_f < 80.0:
            return round(float(v_temp), 2)

        v_hi_f = (
            -42.379
            + (2.04901523 * v_temp_f)
            + (10.14333127 * v_humidity)
            - (0.22475541 * v_temp_f * v_humidity)
            - (0.00683783 * (v_temp_f**2))
            - (0.05481717 * (v_humidity**2))
            + (0.00122874 * (v_temp_f**2) * v_humidity)
            + (0.00085282 * v_temp_f * (v_humidity**2))
            - (0.00000199 * (v_temp_f**2) * (v_humidity**2))
        )

        v_hi_c = (v_hi_f - 32.0) * (5.0 / 9.0)
        return round(float(v_hi_c), 2)

    transformed_df = fct_df.with_column(
        "heat_index_celsius",
        index_calculation(
            F.col("HUMIDITY"),
            F.col("PRESSURE"),
            F.col("TEMP_CELSIUS")
        )
    )

    return transformed_df