from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "suvendu",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email": ["suvendusahani145@gmail.com"],
    "email_on_retry": False,
    "email_on_failure": False,
    "depends_on_past": False,
}

with DAG(
    dag_id="snowflake_test_connection",
    default_args=default_args,
    start_date=datetime(2025, 9, 9),
    schedule="*/15 * * * *",
    catchup=False,
) as dag:

    test_connection = SnowflakeOperator(
        task_id="test_connection",
        snowflake_conn_id="snowflake_conn",
        sql="""
            SELECT
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE();
        """
    )