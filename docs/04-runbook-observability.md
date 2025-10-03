
# Observability – Prometheus, ServiceMonitor, Grafana

- The agent exports metrics with `prometheus_client.start_http_server(port)` (default **9100**). citeturn0search4  
- You can serve **HTTPS** metrics by providing `certfile`/`keyfile`. citeturn0search12  
- Prometheus Operator scrapes via **ServiceMonitor**; rules via **PrometheusRule** CRD (both included in the chart). citeturn0search21turn0search5

### Dashboard
We ship a ConfigMap labeled so Grafana’s sidecar auto‑loads dashboards. (Common pattern in kube‑prometheus‑stack.) citeturn1search10turn1search5
