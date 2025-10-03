from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {"owner":"airflow","retries":1,"retry_delay": timedelta(minutes=5)}
with DAG("retrain_model", start_date=datetime(2025,1,1), schedule_interval="@daily", catchup=False, default_args=default_args) as dag:
    def _train():
        print("Placeholder: train model, log to MLflow, register new version")
    PythonOperator(task_id="train_model", python_callable=_train)
