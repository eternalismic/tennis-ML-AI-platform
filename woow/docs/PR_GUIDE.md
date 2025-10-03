
# PR Guide — Extended

```bash
git checkout -b feat/agent-mode-observability
unzip woow-agent-pr-extended.zip -d .
git add agents/ charts/ grafana/ airflow/ docker/ docs/ gitops/ requirements_agent.txt .github/workflows/agent-ci.yml
git commit -m "feat(agent): MCP agent + metrics + PrometheusRule + OpenShift UWM docs & diagrams"
git push origin feat/agent-mode-observability
```
Open a PR and link to:
- `docs/00-architecture-overview.md`
- `docs/ai-ml-explained.md`
- `docs/03-runbook-openshift-uwm.md`
- `docs/04-runbook-observability.md`
