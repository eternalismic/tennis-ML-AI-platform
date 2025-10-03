
# Runbook — SIM / Shadow

1. Deploy Helm chart with `agent.mode=SIM`.
2. Confirm `/metrics` scraped; Grafana dashboard shows evaluations.
3. Verify `/api/sse` streams events into UI; Decision Feed updates.
4. Tune thresholds with a small set of tournaments.
5. Review daily: bets count, ROI, edge distributions.
