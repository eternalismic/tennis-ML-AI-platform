
# OpenShift Notes

- Enable **User Workload Monitoring (UWM)** to scrape app namespaces.
- Confirm **ServiceMonitor** target is discovered under *Observe → Targets*.
- Use a Route to expose the UI; prefer edge termination TLS.
- RBAC & SecurityContextConstraints may require tuning for images.
