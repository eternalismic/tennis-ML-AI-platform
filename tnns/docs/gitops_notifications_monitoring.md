# GitOps: Notifications, Monitoring & Operators

This pack adds:
1. **Argo CD Notifications** (Slack + Email) via `argocd-notifications-cm` and secret.
2. **Monitoring**: ServiceMonitors for Prediction API and Strimzi Kafka Exporter + Grafana dashboard for the API.
3. **OLM Subscriptions**: Strimzi Kafka Operator and CloudNativePG via OperatorHub (community-operators).

Subscribe Argo CD apps using annotations:
```
notifications.argoproj.io/subscribe.on-sync-succeeded.slack: "#tnns-gitops"
notifications.argoproj.io/subscribe.on-sync-failed.email: "mlops@example.com"
```
