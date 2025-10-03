from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
def promote(): os.system('python -m src.pipeline.promote_and_update_gitops')
with DAG(dag_id="promote_model", start_date=datetime(2025,1,1), schedule_interval=None,
         catchup=False, default_args={"retries":1,"retry_delay":timedelta(minutes=5)}) as dag:
    PythonOperator(task_id="promote_and_update_gitops", python_callable=promote)
