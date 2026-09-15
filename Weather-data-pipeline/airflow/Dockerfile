FROM apache/airflow:2.9.1-python3.9

# Switch to root only if you need to run apt-get install (like git, curl, etc.)
USER root
RUN apt-get update && apt-get install -y git patch && rm -rf /var/lib/apt/lists/*

# Now switch to the airflow user before installing Python packages
USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt