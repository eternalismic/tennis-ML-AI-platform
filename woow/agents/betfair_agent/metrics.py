
from prometheus_client import Counter, Gauge, Histogram, start_http_server

MCP_EVALS = Counter("mcp_evaluations_total", "MCP evaluations")
MCP_RECS = Counter("mcp_recommendations_total", "MCP recommendations", ["rec"])
ORDERS_PLACED = Counter("orders_placed_total", "Orders placed", ["side"])
ORDERS_MATCHED = Counter("orders_matched_total", "Orders matched", ["side"])

EDGE_OBS = Histogram("mcp_edge", "Observed MCP edge when acting", buckets=[0.0,0.02,0.05,0.1,0.2,0.5,1.0])

PENDING_EXPOSURE = Gauge("pending_exposure", "Open unmatched exposure (approx)")
BANKROLL = Gauge("bankroll_current", "Configured bankroll baseline for stake sizing")
PNL_TOTAL = Gauge("pnl_total", "Cumulative P/L (simulated within process)")
ROI = Gauge("roi_total", "Cumulative ROI = pnl / stake_outlay")
DAILY_BETS = Gauge("daily_bets", "Bets placed today")
DAILY_PNL = Gauge("daily_pnl", "P/L today (resets externally)")

def start_metrics_server(port: int = 9100):
    start_http_server(port)
