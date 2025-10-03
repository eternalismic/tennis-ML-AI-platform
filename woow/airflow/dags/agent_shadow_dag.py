
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner":"airflow","retries":0}

with DAG("agent_shadow", start_date=datetime(2025,10,1), schedule_interval=None, catchup=False, default_args=default_args) as dag:
    run_agent = BashOperator(
        task_id="run_agent_sim_24h",
        bash_command="timeout 86400 python -m agents.betfair_agent.run_agent --mode SIM --inplay-only"
    )
