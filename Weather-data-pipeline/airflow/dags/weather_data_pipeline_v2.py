from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="weather_data_pipeline_v2",
    start_date=datetime(2026, 9, 15),
    schedule_interval="*/15 * * * *",
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/weather_data && /home/airflow/.local/bin/dbt run --fail-fast || exit 1"
    )