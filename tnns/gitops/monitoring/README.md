# Monitoring Pack

- **ServiceMonitor** for Prediction API (scrapes `/metrics`).
- **ServiceMonitor** for Strimzi Kafka Exporter (label selector `strimzi.io/name: my-cluster-kafka-exporter`, port `metrics`).
- **Grafana** dashboard ConfigMap for Prediction API.

Import Strimzi community dashboards in Grafana (IDs **11285** and **11271**) for Kafka metrics.
