
import logging
from typing import Optional
import betfairlightweight
from flumine import Flumine, clients
logger = logging.getLogger(__name__)
def build_client(username: str, password: str, app_key: str, certs_dir: Optional[str], mode: str):
    trading = betfairlightweight.APIClient(username=username,password=password,app_key=app_key,certs=certs_dir if certs_dir else None)
    client = clients.BetfairClient(trading, lightweight=False, paper_trade=(mode.upper() != "REAL"))
    return trading, client
def run_framework(framework: Flumine):
    client = framework.client; trading: betfairlightweight.APIClient = client.trading
    try:
        trading.login(); framework.run()
    finally:
        try: trading.logout()
        except Exception: pass
