import json, os, time, random, logging
from typing import Dict, Any
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("odds-ingestion")

bootstrap = os.getenv("KAFKA_BOOTSTRAP","kafka:9092")
topic = os.getenv("ODDS_TOPIC","odds")
provider = os.getenv("ODDS_PROVIDER","MOCK").upper()

producer = KafkaProducer(
    bootstrap_servers=bootstrap,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish(payload: Dict[str, Any]):
    producer.send(topic, payload)
    producer.flush()

def run_mock():
    match = os.getenv("MATCH","PlayerA vs PlayerB")
    p1 = os.getenv("PLAYER1","PlayerA")
    p2 = os.getenv("PLAYER2","PlayerB")
    base1 = float(os.getenv("BASE_ODDS_1","1.85"))
    base2 = float(os.getenv("BASE_ODDS_2","2.00"))
    interval = float(os.getenv("INTERVAL","5"))
    log.info("[MOCK] Publishing to %s every %.1fs", topic, interval)
    while True:
        payload = {
            "provider": "MOCK",
            "match": match,
            "player1": p1,
            "player2": p2,
            "player1_odds": round(max(1.01, base1 + random.uniform(-0.10,0.10)), 2),
            "player2_odds": round(max(1.01, base2 + random.uniform(-0.10,0.10)), 2),
            "ts": time.time()
        }
        publish(payload); time.sleep(interval)

def run_theoddsapi():
    import requests
    api_key = os.getenv("ODDS_API_KEY")
    sport_key = os.getenv("ODDS_SPORT_KEY","tennis_atp")
    regions = os.getenv("ODDS_REGIONS","eu,uk")
    markets = os.getenv("ODDS_MARKETS","h2h")
    interval = float(os.getenv("INTERVAL","30"))
    if not api_key:
        log.error("ODDS_API_KEY not set"); time.sleep(10); return
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
    log.info("[TheOddsAPI] polling %s every %.1fs", url, interval)
    while True:
        try:
            r = requests.get(url, params={"apiKey": api_key, "regions": regions, "markets": markets})
            r.raise_for_status()
            for ev in r.json():
                bms = ev.get("bookmakers") or []
                if not bms: continue
                mkts = bms[0].get("markets") or []
                if not mkts: continue
                outs = mkts[0].get("outcomes") or []
                if len(outs) < 2: continue
                p1o = float(outs[0].get("price") or 0)
                p2o = float(outs[1].get("price") or 0)
                payload = {
                    "provider": "THE_ODDS_API",
                    "match": f"{ev.get('home_team','?')} vs {ev.get('away_team','?')}",
                    "player1": outs[0].get("name","P1"),
                    "player2": outs[1].get("name","P2"),
                    "player1_odds": p1o,
                    "player2_odds": p2o,
                    "commence_time": ev.get("commence_time"),
                    "ts": time.time()
                }
                publish(payload)
        except Exception as e:
            log.exception("TheOddsAPI error: %s", e)
        time.sleep(interval)

def run_betfair():
    import betfairlightweight
    username = os.getenv("BETFAIR_USERNAME")
    password = os.getenv("BETFAIR_PASSWORD")
    app_key = os.getenv("BETFAIR_APP_KEY")
    cert_file = os.getenv("BETFAIR_CERT_FILE")
    key_file = os.getenv("BETFAIR_KEY_FILE")
    event_type_id = os.getenv("BETFAIR_EVENT_TYPE_ID","2")
    if not (username and password and app_key):
        log.error("Betfair credentials not set"); time.sleep(10); return
    client = betfairlightweight.APIClient(
        username=username, password=password, app_key=app_key,
        certs=(os.path.dirname(cert_file) if cert_file else None)
    )
    try:
        if cert_file and key_file:
            client.login_interactive = False
            client.session.cert = (cert_file, key_file)
        client.login()
        log.info("[Betfair] Logged in as %s", username)
        market_filter = betfairlightweight.filters.market_filter(
            event_type_ids=[event_type_id], market_type_codes=["MATCH_ODDS"]
        )
        catalogue = client.betting.list_market_catalogue(
            filter=market_filter, max_results=50, market_projection=["RUNNER_DESCRIPTION","EVENT"]
        )
        market_ids = [m.market_id for m in catalogue]
        if not market_ids:
            log.info("[Betfair] no markets"); time.sleep(30); return
        books = client.betting.list_market_book(market_ids=market_ids, price_projection=betfairlightweight.filters.price_projection())
        for book in books:
            cat = next((c for c in catalogue if c.market_id == book.market_id), None)
            if not cat: continue
            if len(cat.runners) < 2: continue
            r1, r2 = cat.runners[0], cat.runners[1]
            def best_price(rb): 
                try: return float(rb.ex.available_to_back[0].price)
                except Exception: return 0.0
            rb1 = next((rb for rb in book.runners if rb.selection_id == r1.selection_id), None)
            rb2 = next((rb for rb in book.runners if rb.selection_id == r2.selection_id), None)
            p1o = best_price(rb1) if rb1 else 0.0
            p2o = best_price(rb2) if rb2 else 0.0
            payload = {
                "provider": "BETFAIR",
                "match": cat.event.name,
                "player1": r1.runner_name,
                "player2": r2.runner_name,
                "player1_odds": round(p1o, 2),
                "player2_odds": round(p2o, 2),
                "betfair_market_id": book.market_id,
                "player1_selection_id": r1.selection_id,
                "player2_selection_id": r2.selection_id,
                "inplay": book.inplay,
                "ts": time.time()
            }
            publish(payload)
    except Exception as e:
        log.exception("Betfair error: %s", e)
    finally:
        try: client.logout()
        except Exception: pass

if __name__ == "__main__":
    log.info("Starting odds ingestion provider=%s", provider)
    if provider == "BETFAIR":
        while True: run_betfair(); time.sleep(30)
    elif provider in ("ODDS_API","THE_ODDS_API"):
        run_theoddsapi()
    else:
        run_mock()
