#!/usr/bin/env bash
set -euo pipefail
: "${REPO_URL:?Usage: REPO_URL=https://github.com/<you>/infra-odh.git scripts/set_repo_url.sh}"
for f in argocd/bootstrap/*.yaml argocd/applications/*/*.yaml ; do
  sed -i.bak "s#{{ REPO_URL }}#${REPO_URL}#g" "$f"
done
echo "[+] Injected REPO_URL into Argo CD manifests."
