# Providers
- **ROSA**: use `rhcs` Terraform provider + `rosa` CLI. Configure STS/OIDC. Apply in `terraform/aws-rosa`.
- **ARO**: use `azurerm_redhat_openshift_cluster`. Provide domain and pull secret. Apply in `terraform/azure-aro`.
- **OKD**: GCP scaffolding + OKD installer script.
