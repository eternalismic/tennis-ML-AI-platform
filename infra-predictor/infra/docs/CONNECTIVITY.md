# Connectivity
- **external-dns**: Google provider. Create `external-dns-gcp` secret with SA JSON.
- **TLS**: OpenShift Routes have edge TLS by default. On k8s, use cert-manager Issuers.
- **OAuth Proxies**: MLflow and Airflow guarded via OpenShift OAuth proxy deployments and Routes.
