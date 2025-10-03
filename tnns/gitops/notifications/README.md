# Argo CD Notifications (Slack + Email)

1. Create `argocd-notifications-secret` (or a SealedSecret).
2. Apply `argocd-notifications-cm.yaml` and the Secret in `openshift-gitops` ns.
3. Subscribe Applications via annotations:
```
notifications.argoproj.io/subscribe.on-sync-succeeded.slack: "#tnns-gitops"
notifications.argoproj.io/subscribe.on-sync-failed.email: "mlops@example.com"
```
