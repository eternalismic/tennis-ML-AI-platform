
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner":"airflow","retries":0}

THRESHOLDS = [0.02, 0.05, 0.08, 0.1]

with DAG("mcp_threshold_sweep", start_date=datetime(2025,10,1), schedule_interval=None, catchup=False, default_args=default_args) as dag:
    for th in THRESHOLDS:
        BashOperator(
            task_id=f"sim_th_{str(th).replace('.','_')}",
            bash_command=f"MCP_EDGE_THRESHOLD={th} timeout 14400 python -m agents.betfair_agent.run_agent --mode SIM --inplay-only"
        )
