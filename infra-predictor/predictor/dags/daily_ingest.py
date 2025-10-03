from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
def ingest_odds(): print("TODO: fetch odds and persist")
def ingest_scores(): print("TODO: fetch live scores and persist")
with DAG(dag_id="daily_ingest", start_date=datetime(2025,1,1), schedule_interval="@daily",
         catchup=False, default_args={"retries":1,"retry_delay":timedelta(minutes=5)}) as dag:
    PythonOperator(task_id="ingest_odds", python_callable=ingest_odds) >>     PythonOperator(task_id="ingest_scores", python_callable=ingest_scores)
