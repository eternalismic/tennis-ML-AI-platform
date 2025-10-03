import time, random
def fetch_live_odds_stream(market_id: str):
    p=0.5
    while True:
        p = max(0.01, min(0.99, p + random.uniform(-0.01,0.01)))
        yield (time.time(), p)
        time.sleep(1)
