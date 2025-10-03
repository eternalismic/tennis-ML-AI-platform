
import argparse, os, logging
from .config import AgentConfig
from .mcp import MCP
from .strategy import MCPTennisStrategy, StrategyParams, tennis_market_filter, market_data_filter
from .executor import build_client, run_framework
from .metrics import start_metrics_server
from flumine import Flumine
logging.basicConfig(level=os.getenv("AGENT_LOG_LEVEL", "INFO"))
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["SIM","REAL"], default=os.getenv("AGENT_MODE","SIM"))
    p.add_argument("--min-odds", type=float, default=float(os.getenv("MCP_MIN_ODDS","1.01")))
    p.add_argument("--max-odds", type=float, default=float(os.getenv("MCP_MAX_ODDS","1000.0")))
    p.add_argument("--edge-threshold", type=float, default=float(os.getenv("MCP_EDGE_THRESHOLD","0.05")))
    p.add_argument("--max-risk-pct", type=float, default=float(os.getenv("MCP_MAX_RISK_PCT","0.01")))
    p.add_argument("--bankroll", type=float, default=float(os.getenv("MCP_BANKROLL","1000.0")))
    p.add_argument("--inplay-only", action="store_true")
    p.add_argument("--market-types", default=os.getenv("MARKET_TYPES","MATCH_ODDS"))
    p.add_argument("--event-type-ids", default=os.getenv("EVENT_TYPE_IDS","2"))
    p.add_argument("--metrics-port", type=int, default=int(os.getenv("METRICS_PORT","9100")))
    p.add_argument("--daily-stop-loss", type=float, default=float(os.getenv("DAILY_STOP_LOSS","100.0")))
    p.add_argument("--daily-take-profit", type=float, default=float(os.getenv("DAILY_TAKE_PROFIT","1000.0")))
    p.add_argument("--daily-max-bets", type=int, default=int(os.getenv("DAILY_MAX_BETS","200")))
    a = p.parse_args()
    cfg = AgentConfig()
    cfg.mode, cfg.min_odds, cfg.max_odds = a.mode, a.min_odds, a.max_odds
    cfg.edge_threshold, cfg.max_risk_pct, cfg.bankroll = a.edge_threshold, a.max_risk_pct, a.bankroll
    cfg.inplay_only, cfg.market_types, cfg.event_type_ids = a.inplay_only, a.market_types, a.event_type_ids
    cfg.metrics_port, cfg.daily_stop_loss, cfg.daily_take_profit, cfg.daily_max_bets = a.metrics_port, a.daily_stop_loss, a.daily_take_profit, a.daily_max_bets
    start_metrics_server(cfg.metrics_port)
    mcp = MCP(cfg.prediction_api_url, cfg.prediction_api_key)
    trading, client = build_client(cfg.bf_username, cfg.bf_password, cfg.bf_app_key, cfg.certs_path(), cfg.mode)
    framework = Flumine(client=client)
    params = StrategyParams(edge_threshold=cfg.edge_threshold, max_risk_pct=cfg.max_risk_pct, bankroll=cfg.bankroll,
                            min_odds=cfg.min_odds, max_odds=cfg.max_odds, daily_stop_loss=cfg.daily_stop_loss,
                            daily_take_profit=cfg.daily_take_profit, daily_max_bets=cfg.daily_max_bets)
    strat = MCPTennisStrategy(mcp=mcp, params=params,
                              market_filter=tennis_market_filter(event_type_ids=[x.strip() for x in cfg.event_type_ids.split(",")],
                                                                 inplay_only=cfg.inplay_only,
                                                                 market_types=[x.strip() for x in cfg.market_types.split(",")]),
                              market_data_filter=market_data_filter(), name="MCPTennisStrategy")
    framework.add_strategy(strat)
    run_framework(framework)
if __name__ == "__main__": main()
