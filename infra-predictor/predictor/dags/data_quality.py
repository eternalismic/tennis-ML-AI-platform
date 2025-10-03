from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
def run_gx(): os.system('python -m src.quality.run_gx')
with DAG(dag_id="data_quality", start_date=datetime(2025,1,1), schedule_interval="@daily",
         catchup=False, default_args={"retries":1,"retry_delay":timedelta(minutes=5)}) as dag:
    PythonOperator(task_id="great_expectations", python_callable=run_gx)
