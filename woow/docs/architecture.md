
# Architecture (Big Picture)

```mermaid
flowchart LR
  subgraph UI["Next.js UI"]
    A1["MCP Console<br/>SSE Edge Chart"]
    A2["/api/sse & /api/simulate proxies"]
  end
  subgraph GW["UI Gateway (FastAPI)"]
    G1["/api/events (SSE)"]
    G2["/simulate (dry-run)"]
    G3["/api/metrics_summary (Prom API)"]
  end
  subgraph Agent["Agent (Flumine + Model)"]
    S1["Stream API (odds)"]
    S2["MCP evaluate<br/>edge & decision"]
    S3["Prometheus /metrics"]
    S4["Events JSONL"]
  end
  subgraph Obs["Observability"]
    P["Prometheus"]
    Gr["Grafana"]
  end
  UI -->|"SSE proxy"| GW
  GW -->|"tail events"| Agent
  Agent -->|"metrics"| P
  P --> Gr
  GW -->|"Prom HTTP API"| P
  Agent -->|"orders"| BF[(Betfair Exchange)]
  Agent -->|"Prediction API (optional)"| MODEL[(Prediction Service)]
  GW --> UI
```

**Why this design?**

- The **UI** uses server-side proxies so tokens live in cookies (no secrets in the browser).
- The **Gateway** unifies live streaming (SSE), simulation previews, and metrics.
- The **Agent** stays focused on market + model logic, emitting events & metrics.
- **Prometheus/Grafana** provide transparent, real-time observability.
