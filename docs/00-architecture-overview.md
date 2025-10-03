
# Architecture Overview (with pictures)

> **Purpose**: a responsive, safe, and observable tennis betting agent that reacts to live odds, compares them to model **fair odds**, and places value bets with strict risk limits.

## Diagram – Big Picture

```mermaid
flowchart LR
  BF[Betfair Exchange
Stream API] -->|prices, order updates| Agent
  subgraph Agent[Agent (Flumine + MCP)]
    S[Strategy
(MCPTennisStrategy)]
    M[MCP
(fair odds & edge)]
    R[Risk & Circuit Breakers]
    E[Executor
(place/cancel)]
    S --> M --> R --> E
  end
  Agent -->|/metrics| Prom[Prometheus]
  Prom --> Grafana[Grafana Dashboard]
  Agent -->|optional| PredAPI[Prediction API
(prob_a, prob_b)]
```

- **Stream API** feeds low‑latency market updates; we avoid expensive REST polling. citeturn0search3turn0search19  
- **Flumine** hosts our Strategy, consumes the stream, and handles paper/real execution. citeturn0search0turn0search16  
- **MCP** converts probabilities → fair odds and finds **edge**; stake sizing via capped Kelly.  
- **Prometheus & Grafana** expose health and performance (P/L, ROI, exposure). citeturn0search4turn0search21
