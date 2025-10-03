
# OpenShift – User Workload Monitoring (with screenshots)

1) **Enable UWM** by setting `enableUserWorkload: true` in `cluster-monitoring-config` (namespace `openshift-monitoring`). citeturn0search15  
2) Deploy our chart (Service + ServiceMonitor). Prometheus UWM will discover and scrape `/metrics`. citeturn0search21  
3) Open the web console → **Observe → Targets**; you should see the agent target (see figure in this article).  
   ![Targets](https://developers.redhat.com/articles/2023/08/08/how-monitor-workloads-using-openshift-monitoring-stack) citeturn2search2

**Tips**
- Check your namespace is **not excluded** from UWM: no label `openshift.io/user-monitoring=false`. citeturn2search6
- You can attach **PrometheusRule** alerts; OpenShift shows alerts under **Observe → Alerting**. citeturn2search0
