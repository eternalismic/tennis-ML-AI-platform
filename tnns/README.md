# TNNS-CMPT-PWR (Local-first → OpenShift, GitOps-ready)

This repository provides a **local-first** scaffold for the tennis analytics platform, extended to production with OpenShift and Argo CD GitOps.

It includes:
- Docker Compose for local development (PostgreSQL, MinIO, MLflow, Kafka/ZooKeeper, Prometheus, Grafana, services)
- Services: Prediction API (MLflow-backed), MCP agent, Odds ingestion (real providers), Betting execution (sim/Betfair)
- Airflow (standalone dev mode) with a sample DAG
- Helm chart (custom services + optional MLflow/MinIO/Airflow) and example Strimzi/CNPG CRs
- Terraform module to install the Helm chart
- Argo CD GitOps skeleton (operators, infra, data, app, monitoring, notifications)
- Detailed docs in `/docs`

See `/docs` and `/gitops/README.md` for details.
