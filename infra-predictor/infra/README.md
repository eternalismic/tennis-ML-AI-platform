# infra-odh (extended) — OpenShift/OKD + Open Data Hub + GitOps + Providers + Security

This repo bootstraps **Open Data Hub** on **OpenShift/OKD** across environments (local/CRC, GCP OKD, AWS/ROSA, Azure/ARO, on‑prem).
It uses **Terraform** (infra scaffolding), **Argo CD** (GitOps), and **Helm** (ODH & apps).

**Includes**: Sealed Secrets, CloudNativePG (Postgres), kube-prometheus-stack, MinIO, MLflow, Airflow (GitSync), **KServe**, **Argo Rollouts**, **tennis-predictor**, CNPG **tennis-data-db**, **NetworkPolicies**, **OAuth proxies**, **external-dns**, **cert-manager**, and dashboards.
