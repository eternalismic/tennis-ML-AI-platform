
# Alerts & SLOs

We include a `PrometheusRule` template with:
- **AgentDailyStopLossBreached** – fires when `daily_pnl` <= −X for 5m  
- **AgentNoData** – no MCP evals for 15m  
- **AgentHighExposure** – pending exposure > threshold for 10m

These are picked up automatically by Prometheus Operator. citeturn0search5turn0search6
