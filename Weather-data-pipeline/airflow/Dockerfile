FROM apache/airflow:2.9.1-python3.9

USER root
RUN apt-get update && apt-get install -y git patch

USER airflow

COPY requirements.txt .

# Install main requirements with constraints
RUN pip install --no-cache-dir \
--constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.9.txt \
apache-airflow-providers-snowflake

# Install dbt-snowflake separately without constraints to avoid dependency locking clashes
RUN pip install --no-cache-dir dbt-snowflake