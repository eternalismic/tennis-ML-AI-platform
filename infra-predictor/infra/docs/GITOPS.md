# GitOps
- Root apps in `argocd/bootstrap/<env>-root-app.yaml`.
- Child apps in `argocd/applications/<env>/apps.yaml` and siblings (db, dashboards, kserve, security).
- After editing values or charts, commit → Argo auto-syncs.
