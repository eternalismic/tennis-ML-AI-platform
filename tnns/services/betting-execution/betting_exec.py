import json, os, logging
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("bet-exec")

bootstrap = os.getenv("KAFKA_BOOTSTRAP","kafka:9092")
topic = os.getenv("PRED_TOPIC","predictions")
group_id = os.getenv("GROUP_ID","bet-exec")
threshold = float(os.getenv("EDGE_THRESHOLD","0.05"))

bankroll = float(os.getenv("BANKROLL","1000"))
max_fraction = float(os.getenv("MAX_STAKE_FRACTION","0.02"))
base_stake = float(os.getenv("BASE_STAKE","10"))
commission = float(os.getenv("COMMISSION_RATE","0.05"))
exec_mode = os.getenv("EXECUTION_MODE","SIM").upper()

bf_username = os.getenv("BETFAIR_USERNAME")
bf_password = os.getenv("BETFAIR_PASSWORD")
bf_app_key = os.getenv("BETFAIR_APP_KEY")
bf_cert_file = os.getenv("BETFAIR_CERT_FILE")
bf_key_file = os.getenv("BETFAIR_KEY_FILE")

def compute_stake(edge: float) -> float:
    stake = min(base_stake, bankroll * max_fraction)
    stake *= max(0.5, min(1.5, 1.0 + (edge - threshold)))
    return round(max(2.0, stake), 2)

class BetfairClient:
    def __init__(self):
        import betfairlightweight
        self.bfl = betfairlightweight
        self.client = self.bfl.APIClient(
            username=bf_username, password=bf_password, app_key=bf_app_key,
            certs=(os.path.dirname(bf_cert_file) if bf_cert_file else None)
        )
    def __enter__(self):
        if bf_cert_file and bf_key_file:
            self.client.login_interactive = False
            self.client.session.cert = (bf_cert_file, bf_key_file)
        self.client.login()
        return self.client
    def __exit__(self, exc_type, exc, tb):
        try: self.client.logout()
        except Exception: pass

def place_bet_betfair(match: str, selection_name: str, market_id: str, selection_id: int, price: float, size: float):
    import betfairlightweight
    with BetfairClient() as cli:
        order = betfairlightweight.filters.place_instruction(
            selection_id=selection_id, order_type="LIMIT",
            side="BACK", limit_order=betfairlightweight.filters.limit_order(price=price, size=size, persistence_type="PERSIST")
        )
        resp = cli.betting.place_orders(market_id=market_id, instructions=[order])
        status = resp.status
        logging.info("BETFAIR place_orders status=%s matched=%s", status, getattr(resp, "instruction_reports", None))
        return status

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=group_id,
)

log.info("[EXEC] mode=%s edge_threshold=%.3f bankroll=%.2f", exec_mode, threshold, bankroll)
for msg in consumer:
    d = msg.value or {}
    ev_a = float(d.get("model_prob_a") or 0) - float(d.get("market_prob_a") or 0)
    ev_b = float(d.get("model_prob_b") or 0) - float(d.get("market_prob_b") or 0)
    pick = None; edge = 0.0; odds = 0.0; selection_id=None; market_id=None; sel_name=None
    if ev_a > threshold:
        pick = "A"; edge = ev_a; odds = float(d.get("p1_odds") or 0); sel_name = d.get("player1")
        selection_id = d.get("player1_selection_id")
    elif ev_b > threshold:
        pick = "B"; edge = ev_b; odds = float(d.get("p2_odds") or 0); sel_name = d.get("player2")
        selection_id = d.get("player2_selection_id")
    if not pick:
        log.info("NO BET: edges A=%.3f, B=%.3f", ev_a, ev_b); continue

    stake = compute_stake(edge)
    market_id = d.get("betfair_market_id")
    match = d.get("match","?")

    if exec_mode == "BETFAIR":
        if not all([bf_username, bf_password, bf_app_key]):
            log.error("BETFAIR mode but missing credentials"); continue
        if not (market_id and selection_id):
            log.error("BETFAIR execution requires market_id and selection_id in message"); continue
        try:
            status = place_bet_betfair(match, sel_name, str(market_id), int(selection_id), float(odds), float(stake))
            log.info("BET EXECUTED: %s on %s @ %.2f stake %.2f (status=%s)", sel_name, match, odds, stake, status)
        except Exception as e:
            log.exception("Betfair execution failed: %s", e)
    else:
        log.info("SIM BET: BACK %s on %s @ %.2f stake %.2f (edge=%.3f)", sel_name, match, odds, stake, edge)
