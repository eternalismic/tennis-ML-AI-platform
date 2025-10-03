# GCP OKD Install (IPI)
1) `terraform/gcp-okd` → VPC, DNS zone, GCS bucket, APIs.
2) `scripts/gcp_okd_install.sh` → run OKD installer (requires `openshift-install`).
3) `scripts/bootstrap_argocd.sh gcp` + apply root app.
4) Create `external-dns-gcp` Secret with DNS admin SA JSON.
