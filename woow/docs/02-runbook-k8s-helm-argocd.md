
# Runbook – Kubernetes (Helm) & GitOps (Argo CD)

## Helm quickstart (SIM)
```bash
helm upgrade --install tennis charts/tennis -n tennis-dev --create-namespace   --set agent.mode=SIM   --set agent.serviceMonitor.enabled=true   --set agent.grafanaDashboard.enabled=true
```

## Argo CD (valuesObject)
Point the Application at `charts/tennis` and use inline `valuesObject` to set env‑specific values. citeturn1search0

```yaml
spec:
  source:
    helm:
      valuesObject:
        agent:
          mode: SIM
          serviceMonitor: { enabled: true, release: prometheus }
```
