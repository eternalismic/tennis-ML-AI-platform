
# Diagram Gallery (Mermaid)

## Big Picture
```mermaid
flowchart LR
  Exchange[(Betfair Exchange)] --> StreamAPI[Stream API]
  StreamAPI --> Agent[Agent Service]
  Agent -->|/metrics| Prometheus
  Prometheus --> Grafana
  Agent -->|orders| Exchange
  Agent -->|optional| PredictionAPI
```

## Data & Decisions
```mermaid
flowchart LR
  Prices[Best back prices] --> MCP
  Probs[Model probs] --> MCP
  MCP --> Edge[Edge >= threshold?]
  Edge -->|Yes| Stake[Kelly-sized stake]
  Stake --> Order[Place limit order]
  Edge -->|No| Wait[No bet]
```
