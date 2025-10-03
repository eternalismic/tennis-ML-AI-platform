
import argparse, os, logging
from .config import AgentConfig
from .mcp import MCP
from .strategy import MCPTennisStrategy, StrategyParams, tennis_market_filter, market_data_filter
from .executor import build_client, run_framework
from .metrics import start_metrics_server
from flumine import Flumine

logging.basicConfig(level=os.getenv("AGENT_LOG_LEVEL", "INFO"))
logger = logging.getLogger("betfair_agent")

def main():
    parser = argparse.ArgumentParser(description="Run MCP Tennis Agent (Flumine)")
    parser.add_argument("--mode", choices=["SIM","REAL"], default=os.getenv("AGENT_MODE","SIM"))
    parser.add_argument("--min-odds", type=float, default=float(os.getenv("MCP_MIN_ODDS","1.01")))
    parser.add_argument("--max-odds", type=float, default=float(os.getenv("MCP_MAX_ODDS","1000.0")))
    parser.add_argument("--edge-threshold", type=float, default=float(os.getenv("MCP_EDGE_THRESHOLD","0.05")))
    parser.add_argument("--max-risk-pct", type=float, default=float(os.getenv("MCP_MAX_RISK_PCT","0.01")))
    parser.add_argument("--bankroll", type=float, default=float(os.getenv("MCP_BANKROLL","1000.0")))
    parser.add_argument("--inplay-only", action="store_true")
    parser.add_argument("--market-types", default=os.getenv("MARKET_TYPES","MATCH_ODDS"))
    parser.add_argument("--event-type-ids", default=os.getenv("EVENT_TYPE_IDS","2"))
    parser.add_argument("--metrics-port", type=int, default=int(os.getenv("METRICS_PORT","9100")))
    parser.add_argument("--daily-stop-loss", type=float, default=float(os.getenv("DAILY_STOP_LOSS","100.0")))
    parser.add_argument("--daily-take-profit", type=float, default=float(os.getenv("DAILY_TAKE_PROFIT","1000.0")))
    parser.add_argument("--daily-max-bets", type=int, default=int(os.getenv("DAILY_MAX_BETS","200")))
    args = parser.parse_args()

    cfg = AgentConfig()
    cfg.mode = args.mode
    cfg.min_odds = args.min_odds; cfg.max_odds = args.max_odds
    cfg.edge_threshold = args.edge_threshold; cfg.max_risk_pct = args.max_risk_pct
    cfg.bankroll = args.bankroll; cfg.inplay_only = args.inplay_only
    cfg.market_types = args.market_types; cfg.event_type_ids = args.event_type_ids
    cfg.metrics_port = args.metrics_port
    cfg.daily_stop_loss = args.daily_stop_loss; cfg.daily_take_profit = args.daily_take_profit
    cfg.daily_max_bets = args.daily_max_bets

    start_metrics_server(cfg.metrics_port)

    mcp = MCP(cfg.prediction_api_url, cfg.prediction_api_key)

    trading, client = build_client(cfg.bf_username, cfg.bf_password, cfg.bf_app_key, cfg.certs_path(), cfg.mode)
    framework = Flumine(client=client)

    params = StrategyParams(
        edge_threshold=cfg.edge_threshold, max_risk_pct=cfg.max_risk_pct,
        bankroll=cfg.bankroll, min_odds=cfg.min_odds, max_odds=cfg.max_odds,
        daily_stop_loss=cfg.daily_stop_loss, daily_take_profit=cfg.daily_take_profit,
        daily_max_bets=cfg.daily_max_bets
    )

    strat = MCPTennisStrategy(
        mcp=mcp,
        params=params,
        market_filter=tennis_market_filter(event_type_ids=[x.strip() for x in cfg.event_type_ids.split(",")],
                                           inplay_only=cfg.inplay_only,
                                           market_types=[x.strip() for x in cfg.market_types.split(",")]),
        market_data_filter=market_data_filter(),
        name="MCPTennisStrategy",
    )
    framework.add_strategy(strat)
    logger.info("Starting agent in %s mode; metrics on port %s", cfg.mode, cfg.metrics_port)
    run_framework(framework)

if __name__ == "__main__":
    main()
