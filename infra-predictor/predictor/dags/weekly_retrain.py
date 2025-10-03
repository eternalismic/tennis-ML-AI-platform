from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
def retrain(): os.system('python -m src.pipeline.train --csv /opt/data/historical_matches.csv')
with DAG(dag_id="weekly_retrain", start_date=datetime(2025,1,1), schedule_interval="@weekly",
         catchup=False, default_args={"retries":1,"retry_delay":timedelta(minutes=10)}) as dag:
    PythonOperator(task_id="retrain_models", python_callable=retrain)
