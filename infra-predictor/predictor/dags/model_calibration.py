from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
def run_calibration():
    os.system('python -m src.pipeline.calibration_report --pred-csv /opt/data/model_preds.csv --out-json /opt/data/calibration.json --out-png /opt/data/calibration.png')
with DAG(dag_id="model_calibration", start_date=datetime(2025,1,1), schedule_interval="@weekly",
         catchup=False, default_args={"retries":1,"retry_delay":timedelta(minutes=10)}) as dag:
    PythonOperator(task_id="calibration_report", python_callable=run_calibration)
