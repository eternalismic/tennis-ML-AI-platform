# CI/CD
- **Predictor repo** builds container image on tag (GHCR). Optionally updates infra GitOps with new image tag/modelVersion.
- **Infra repo** lints Helm charts on PR. Argo CD auto-syncs and Argo Rollouts gates canaries by Prometheus metrics.
