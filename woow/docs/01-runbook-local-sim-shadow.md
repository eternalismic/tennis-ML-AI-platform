
# Runbook – Local 24h SIM Shadow

**Goal**: run the agent safely against live prices for 24h (paper trading only).

## Steps
```bash
python -m agents.betfair_agent.run_agent --mode SIM --inplay-only
```
- Flumine **paper trading** simulates execution; market data still comes from live stream. citeturn0search0

## Verify
- Visit `http://localhost:9100/metrics` – counters rising means healthy scrape. citeturn0search4
