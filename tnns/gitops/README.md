# GitOps (Argo CD)

Use the app-of-apps in `gitops/base` to bootstrap:
- Operators (OLM Subscriptions): Strimzi, CloudNativePG
- Infra CRs (Kafka & CNPG clusters)
- Data layer (MLflow + MinIO) via this repo chart
- App layer (Prediction API + agents) via this repo chart
- Monitoring pack (ServiceMonitors + dashboards)
- Notifications (Slack/email)

Create a root Application pointing to `gitops/overlays/dev` or `prod`.
