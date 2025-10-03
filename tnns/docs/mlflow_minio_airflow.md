# MLflow, MinIO, Airflow
- MLflow: registry & experiments, stored in Postgres + MinIO S3.
- MinIO: S3 for artifacts (use PVCs in prod).
- Airflow: dev standalone here; prod via official chart/operator (CeleryExecutor + CNPG).
