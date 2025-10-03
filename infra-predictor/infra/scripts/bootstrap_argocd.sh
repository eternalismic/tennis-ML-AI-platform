#!/usr/bin/env bash
set -euo pipefail
ENV="${1:-local}"
echo "[+] Installing OpenShift GitOps (Argo CD) operator..."
cat <<'YAML' | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata: { name: openshift-gitops-operator-group, namespace: openshift-operators }
spec: { targetNamespaces: [openshift-operators] }
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata: { name: openshift-gitops-operator, namespace: openshift-operators }
spec:
  channel: stable
  name: openshift-gitops-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
YAML

echo "[+] Waiting for Argo CD route..."
until oc get route -n openshift-gitops argocd-server >/dev/null 2>&1; do sleep 5; done
oc -n openshift-gitops get pods
echo "[+] Applying root Application for ${ENV}"
oc apply -f "argocd/bootstrap/${ENV}-root-app.yaml"
oc -n openshift-gitops get applications
