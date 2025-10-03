# OpenShift Deployment
1) Install operators (Strimzi & CloudNativePG) via OLM Subscriptions (see gitops/operators/).
2) Apply GitOps root Application to sync infra, data, app, monitoring, notifications.
3) Configure secrets (S3, MLflow DB, Betfair).
