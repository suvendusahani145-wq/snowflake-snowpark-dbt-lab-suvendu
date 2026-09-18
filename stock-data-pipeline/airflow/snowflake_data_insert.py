import json
import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


default_args = {
    'owner': 'suvendu',
    'retries': 4,
    'email': ['suvendusahani145@gmail.com'],
    'email_on_retry': False,
    'email_on_failure': False,
    'depends_on_past': False
}


with DAG(
    dag_id='snowflake_data_insert',
    default_args=default_args,
    start_date=datetime(2026, 8, 9),
    schedule_interval='*/15 * * * *',
    catchup=False
) as dag:

    api_check = HttpSensor(
        task_id='api_check',
        http_conn_id='my_api_conn',
        endpoint='data/2.5/weather?q=Hyderabad&appid=fe50a9e77671d58718605f3d1d31cc4e',
        poke_interval=30,
        timeout=600
    )

    @task
    def extract_data(**context):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather"
            "?q=Hyderabad&appid=fe50a9e77671d58718605f3d1d31cc4e"
        )

        data = response.json()
        return json.dumps(data)

    @task
    def process_and_load_data(raw_json_str: str):
        snowflake_hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")

        insert_sql = """
        INSERT INTO RAW_WEATHER_REPORTS (RAW_PAYLOAD, CITY_NAME)
        SELECT
            PARSE_JSON(%s) AS PAYLOAD,
            PAYLOAD:name::VARCHAR AS CITY_NAME;
        """

        snowflake_hook.run(
            insert_sql,
            parameters=[raw_json_str],
        )

    extracted_data = extract_data()

    api_check >> extracted_data

    process_and_load_data(extracted_data)