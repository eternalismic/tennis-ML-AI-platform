from typing import Iterator, Dict
import os, betfairlightweight

def login():
    username = os.environ["BETFAIR_USERNAME"]
    password = os.environ["BETFAIR_PASSWORD"]
    app_key  = os.environ["BETFAIR_APP_KEY"]
    cert = os.getenv("BETFAIR_CERT_FILE")
    key  = os.getenv("BETFAIR_KEY_FILE")
    trading = betfairlightweight.APIClient(username, password, app_key=app_key, certs=(cert, key) if cert and key else None)
    trading.login()
    return trading

def list_tennis_markets(trading, text_query="Match Odds")->Iterator[Dict]:
    market_filter = betfairlightweight.filters.market_filter(text_query=text_query, event_type_ids=['2'])
    return trading.betting.list_market_catalogue(filter=market_filter, max_results=100, market_projection=["RUNNER_DESCRIPTION","EVENT"])

def price_to_prob(best_back_price: float)->float:
    if best_back_price<=1.0: return 0.999
    return 1.0 / best_back_price
