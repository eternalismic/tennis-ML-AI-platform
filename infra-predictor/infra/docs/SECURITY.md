# Security Hardening
- NetworkPolicies: default deny for MinIO/MLflow/Airflow; allow only from whitelisted namespaces.
- OAuth Proxy: guard MLflow/Airflow Routes with OpenShift OAuth.
- Sealed Secrets for credentials. Prefer internal Services; limit external exposure.
