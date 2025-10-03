
# Helm — Deploying the Stack

```bash
helm upgrade --install tennis charts/tennis -n tennis --create-namespace   --set agent.mode=SIM   --set ui.enabled=true
```
- UI will expose `/api/sse`, `/api/metrics_summary`, `/api/simulate`.
- Configure Ingress + TLS via `.Values.ui.ingress.*`.
- Enable Prometheus Operator for ServiceMonitor/PrometheusRule.
