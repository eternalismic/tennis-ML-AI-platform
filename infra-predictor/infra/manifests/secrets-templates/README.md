# Sealed Secrets templates
1) Create a Secret manifest (plain) *locally* (do not commit):
2) Seal it:
```
kubectl create -f mysecret.yaml -n <ns> --dry-run=client -o json |   kubeseal --controller-namespace=sealed-secrets --controller-name=sealed-secrets -o yaml > mysecret-sealed.yaml
```
3) Commit only `*-sealed.yaml`. Remove plaintext secrets.
