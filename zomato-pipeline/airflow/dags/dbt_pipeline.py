from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dbt_pipeline",
    start_date=datetime(2026, 9, 5),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/zomato && dbt run --fail-fast || exit 1"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/zomato && dbt test --fail-fast || exit 1"
    )

    dbt_log = BashOperator(
        task_id="dbt_log",
        bash_command="cd /opt/zomato && dbt run --fail-fast --log-format json || exit 1"
    )

    # Define full dependency chain
    dbt_run >> dbt_test >> dbt_log
