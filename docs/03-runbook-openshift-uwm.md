
# Runbook – OpenShift User Workload Monitoring (UWM)

**Goal**: let OpenShift scrape the agent via `ServiceMonitor` and visualize in the web console.

## Enable UWM
Edit (or create) the ConfigMap in `openshift-monitoring`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true
```
OpenShift will deploy the user‑workload Prometheus to scrape your namespaces. citeturn0search15turn2search1

## Screenshots (reference)
- Observe → **Targets** shows user workloads after your `ServiceMonitor` is applied (see Figure 2 in this article).  
  ![Targets](https://developers.redhat.com/articles/2023/08/08/how-monitor-workloads-using-openshift-monitoring-stack)  
  (Scroll to *Figure 2* on that page.) citeturn2search2

- Red Hat docs step‑by‑step (with console views).  
  https://docs.redhat.com/.../monitoring/enabling-monitoring-for-user-defined-projects  citeturn0search7

## Troubleshooting
- Ensure the project is **not excluded** (no label `openshift.io/user-monitoring=false`). citeturn2search6
