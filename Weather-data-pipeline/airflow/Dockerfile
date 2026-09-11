FROM apache/airflow:2.9.1-python3.9

USER root
RUN apt-get update && apt-get install -y git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER airflow
