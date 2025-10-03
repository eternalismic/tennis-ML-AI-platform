
# UI & Gateway

The UI centers the **MCP interaction**: players, fair odds, probabilities, edge, and the live recommendation — with sliders to preview decisions.

- **SSE**: streamed via `/api/sse` proxy.
- **Simulate**: posted via `/api/simulate` proxy (tokens stay in cookies).
- **Metrics**: polled via `/api/metrics_summary` proxy.

```mermaid
sequenceDiagram
  participant Browser
  participant UI as Next.js Route (/api/sse)
  participant GW as Gateway (/api/events)
  Browser->>UI: GET /api/sse
  UI->>GW: GET /api/events (Authorization: Bearer ...)
  GW-->>UI: text/event-stream
  UI-->>Browser: text/event-stream
```
