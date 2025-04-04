from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dags.producer_v1 import fetch_real_data
from dags.kafka_consum_n_snowflake_loader import consume_and_insert_weather_data

def fetch_weather():
    fetch_real_data()
    print(f"producer works and fetched data")

def load_to_snowflake():
    consume_and_insert_weather_data()
    print(f"consumer works and loaded data into snowflake")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 1),
}

with DAG('weather_pipeline', default_args=default_args, schedule_interval='@hourly') as dag:
    fetch_task = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_weather
    )

    load_task = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_to_snowflake
    )

fetch_task >> load_task
