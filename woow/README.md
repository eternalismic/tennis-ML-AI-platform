
# Tennis MCP — Mega + Docs

This repository includes:
- **Agent** (SIM/REAL) with Prometheus metrics + JSONL events
- **UI Gateway** (SSE, /simulate, /api/metrics_summary, OIDC)
- **Next.js UI** with secure **/api/sse**, **/api/simulate**, **/api/metrics_summary** proxies
- **Helm** chart (agent + ui + gateway + alerts + dashboard)
- **MkDocs** site with deep ML/AI documentation + diagrams & charts

## Docs (local)
```bash
pip install mkdocs mkdocs-material pymdown-extensions
mkdocs serve
# open http://127.0.0.1:8000
```

## Quick SIM Run (local)
See `docs/runbooks/sim-shadow.md` and `docs/ui.md`.

## Kubernetes
See `docs/helm.md` and `docs/openshift.md`.
