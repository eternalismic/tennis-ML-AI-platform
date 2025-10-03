# tennis-predictor — Models, Service, Connectors, DB, Pipelines

- **Models**: Elo, XGBoost/LogReg (pre-match), Markov set/match, momentum (XGB/GBDT)
- **Service**: FastAPI (`/predict/prematch`, `/predict/live`, `/metrics`), Prometheus metrics + HTTP SLO metrics
- **Connectors**: Betfair (read-only odds via `betfairlightweight`), vendor live scores placeholder
- **DB**: CNPG Postgres (raw→curated), Alembic migrations, SQLAlchemy models
- **Data Quality**: Great Expectations runtime checks (Airflow DAG)
- **Pipelines**: training/evaluation/calibration, MLflow registry promotion + GitOps update, KServe export to MinIO
- **DAGs**: daily_ingest, weekly_retrain, model_calibration, promote_model, data_quality
