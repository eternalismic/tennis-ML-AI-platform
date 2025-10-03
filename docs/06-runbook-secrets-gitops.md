
# Secrets via GitOps

Use **Sealed Secrets** or **External Secrets Operator** to keep credentials out of plaintext Git:
- *Sealed Secrets*: encrypts Secrets client‑side; only the cluster can decrypt.  
- *External Secrets Operator*: syncs from AWS/GCP/Vault to K8s Secrets. citeturn1search6
