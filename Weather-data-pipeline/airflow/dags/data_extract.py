from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.http_sensor import HttpSensor
from airflow.hooks.base import BaseHook
from datetime import datetime, timedelta
import requests, pandas as pd
from airflow import DAG


default_args = {
       'owner': 'suvendu',
       'retries': 2,
       'retry_delay': timedelta(minutes=5),
       'email': ['suvendusajani543@gmail.com'],
       'email_on_retry': True,
       'email_on_failure' : True,
       'depends_on_past': False
       }
       

def extract_api_data(**context):
     response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Hyderabad&appid=fe50a9e77671d58718605f3d1d31cc4e")
     data = response.json()
     pd.DataFrame([data]).to_csv("/tmp/tmp_weather.csv",index=False)
     context['ti'].xcom_push(key='raw_path',value="/tmp/tmp_weather.csv")

def load_to_db(**context):
    conn = BaseHook.get_connection("snowflake_conn")
    print(f"Loading data to Snowflake at {conn.host}")

    
with DAG(
         dag_id = 'weather_data_extraction',
         default_args= default_args,
         start_date = datetime(2026,8,9),
         schedule_interval = '*/15 * * * *',
         catchup = False
         ) as dag:
         
    api_ready = HttpSensor(
                task_id = "check_api",
                http_conn_id = "my_api_conn",
                endpoint = "data/2.5/weather?q=Hyderabad&appid=fe50a9e77671d58718605f3d1d31cc4e",
                response_check = lambda response : "Hyderabad" in response.text,
                poke_interval= 30
                )

    extract_api = PythonOperator(
                        task_id = "extract_api",
                        python_callable = extract_api_data,
                        provide_context =  True
                        )
                     
                     
                     
                     
api_ready >> extract_api
            