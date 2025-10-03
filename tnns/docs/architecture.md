# Architecture Overview
- Prediction API (FastAPI) loads MLflow Production model (S3 artifacts via MinIO)
- Kafka stream: odds-ingestion → MCP → betting-execution
- Airflow orchestrates retraining
- Prometheus & Grafana for observability (ServiceMonitor + dashboards)
- OpenShift: Strimzi (Kafka), CloudNativePG (Postgres), Routes (TLS), Secrets/SealedSecrets
