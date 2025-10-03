#!/usr/bin/env bash
set -euo pipefail
# Env: PROJECT, REGION, ZONES (comma), BASE_DOMAIN, CLUSTER_NAME, PULL_SECRET, SSH_KEY
: "${PROJECT:?}"; : "${REGION:?}"; : "${ZONES:?}"; : "${BASE_DOMAIN:?}"; : "${CLUSTER_NAME:?}"; : "${PULL_SECRET:?}"; : "${SSH_KEY:?}"
WORKDIR=${WORKDIR:-"./_okd"}
mkdir -p "$WORKDIR"
cat > "${WORKDIR}/install-config.yaml" <<YAML
apiVersion: v1
baseDomain: ${BASE_DOMAIN}
metadata: { name: ${CLUSTER_NAME} }
platform: { gcp: { projectID: ${PROJECT}, region: ${REGION}, defaultMachinePlatform: { type: n2-standard-4 } } }
pullSecret: '${PULL_SECRET}'
sshKey: '${SSH_KEY}'
YAML
echo "[+] Running openshift-install (OKD)..."
openshift-install create cluster --dir "${WORKDIR}" --log-level=info
