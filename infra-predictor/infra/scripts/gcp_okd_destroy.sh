#!/usr/bin/env bash
set -euo pipefail
WORKDIR=${WORKDIR:-"./_okd"}
echo "[!] Destroying cluster via openshift-install from ${WORKDIR}"
openshift-install destroy cluster --dir "${WORKDIR}" --log-level=info
