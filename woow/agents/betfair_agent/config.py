
import os
from dataclasses import dataclass
@dataclass
class AgentConfig:
    mode: str = os.getenv("AGENT_MODE", "SIM")
    log_level: str = os.getenv("AGENT_LOG_LEVEL", "INFO")
    bf_username: str = os.getenv("BF_USERNAME", "")
    bf_password: str = os.getenv("BF_PASSWORD", "")
    bf_app_key: str = os.getenv("BF_APP_KEY", "")
    bf_certs_dir: str = os.getenv("BF_CERTS_DIR", "")
    edge_threshold: float = float(os.getenv("MCP_EDGE_THRESHOLD", "0.05"))
    max_risk_pct: float = float(os.getenv("MCP_MAX_RISK_PCT", "0.01"))
    bankroll: float = float(os.getenv("MCP_BANKROLL", "1000.0"))
    min_odds: float = float(os.getenv("MCP_MIN_ODDS", "1.01"))
    max_odds: float = float(os.getenv("MCP_MAX_ODDS", "1000.0"))
    market_types: str = os.getenv("MARKET_TYPES", "MATCH_ODDS")
    event_type_ids: str = os.getenv("EVENT_TYPE_IDS", "2")
    inplay_only: bool = os.getenv("INPLAY_ONLY", "false").lower() == "true"
    prediction_api_url: str = os.getenv("PREDICTION_API_URL", "").strip()
    prediction_api_key: str = os.getenv("PREDICTION_API_KEY", "").strip()
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() == "true"
    metrics_port: int = int(os.getenv("METRICS_PORT", "9100"))
    daily_stop_loss: float = float(os.getenv("DAILY_STOP_LOSS", "100.0"))
    daily_take_profit: float = float(os.getenv("DAILY_TAKE_PROFIT", "1000.0"))
    daily_max_bets: int = int(os.getenv("DAILY_MAX_BETS", "200"))
    events_path: str = os.getenv("AGENT_EVENTS_PATH", "/var/log/agent/events.jsonl")
    def certs_path(self):
        return self.bf_certs_dir if self.bf_certs_dir else None
