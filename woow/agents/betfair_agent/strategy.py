
import logging, datetime
from typing import Optional, List
from dataclasses import dataclass
from flumine import BaseStrategy
from flumine.order.trade import Trade
from flumine.order.order import LimitOrder, OrderStatus
from betfairlightweight.filters import streaming_market_filter, streaming_market_data_filter
from betfairlightweight.resources import MarketBook
from .mcp import MCP, MarketContext
from .metrics import ORDERS_PLACED, ORDERS_MATCHED, EDGE_OBS, PENDING_EXPOSURE, PNL_TOTAL, ROI, BANKROLL, DAILY_BETS, DAILY_PNL
from .events import write_event
logger = logging.getLogger(__name__)
@dataclass
class StrategyParams:
    edge_threshold: float; max_risk_pct: float; bankroll: float; min_odds: float; max_odds: float
    daily_stop_loss: float; daily_take_profit: float; daily_max_bets: int
class MCPTennisStrategy(BaseStrategy):
    def __init__(self, mcp: MCP, params: StrategyParams, **kwargs):
        super().__init__(**kwargs); self.mcp = mcp; self.params = params
        self.total_staked = 0.0; self._rollover_date = datetime.date.today()
        BANKROLL.set(self.params.bankroll)
    def _roll_daily(self):
        today = datetime.date.today()
        if today != self._rollover_date:
            self._rollover_date = today; DAILY_BETS.set(0); DAILY_PNL.set(0)
    def check_market_book(self, market, market_book: MarketBook) -> bool:
        return market_book.status != "CLOSED"
    def _best_back(self, runner) -> Optional[float]:
        try:
            prices = runner.ex.available_to_back; 
            if prices: return prices[0]["price"]
        except Exception: return None
        return None
    def _circuit_breaker_open(self) -> bool:
        if DAILY_PNL._value.get() <= -abs(self.params.daily_stop_loss): return True
        if DAILY_PNL._value.get() >= abs(self.params.daily_take_profit): return True
        if DAILY_BETS._value.get() >= self.params.daily_max_bets: return True
        return False
    def process_market_book(self, market, market_book: MarketBook) -> None:
        try:
            self._roll_daily()
            if self._circuit_breaker_open(): return
            runners = market_book.runners
            if len(runners) < 2: return
            rc = market.market_catalogue
            if not rc or not rc.runners or len(rc.runners) < 2: return
            nameA, nameB = rc.runners[0].runner_name, rc.runners[1].runner_name
            selA, selB = runners[0], runners[1]
            backA, backB = self._best_back(selA), self._best_back(selB)
            ctx = MarketContext(nameA, nameB, backA, None, backB, None, score=None, server=None)
            res = self.mcp.evaluate(ctx, edge_threshold=self.params.edge_threshold)
            write_event("mcp_evaluation", {
                "market_id": market_book.market_id, "players":[nameA,nameB], "backA": backA, "backB": backB,
                "edge": res.edge, "rec": res.rec, "fair_odds":{"A":res.fair_odds_A,"B":res.fair_odds_B},
                "probs":{"A":res.model_prob_A,"B":res.model_prob_B},
            })
            if res.rec == "BACK_A" and backA and self.params.min_odds <= backA <= self.params.max_odds:
                stake = self._stake(res.model_prob_A, backA); 
                if stake>0: self._place_back(market_book.market_id, selA.selection_id, selA.handicap, stake, backA, nameA); EDGE_OBS.observe(res.edge); self.total_staked += stake; DAILY_BETS.set(DAILY_BETS._value.get()+1)
            elif res.rec == "BACK_B" and backB and self.params.min_odds <= backB <= self.params.max_odds:
                stake = self._stake(res.model_prob_B, backB);
                if stake>0: self._place_back(market_book.market_id, selB.selection_id, selB.handicap, stake, backB, nameB); EDGE_OBS.observe(res.edge); self.total_staked += stake; DAILY_BETS.set(DAILY_BETS._value.get()+1)
        except Exception as e:
            logger.exception("Error processing market_book: %s", e)
    def process_orders(self, market, orders: list) -> None:
        for order in orders:
            if order.size_matched and order.size_matched > 0: ORDERS_MATCHED.labels(side=str(order.side)).inc()
        exposure = 0.0
        for order in orders:
            if order.status == OrderStatus.EXECUTABLE and order.size_remaining:
                try: exposure += float(order.size_remaining) * float(order.order_type.price or 0.0)
                except Exception: pass
        PENDING_EXPOSURE.set(exposure)
    def _stake(self, p: float, price: float) -> float:
        b = max(price-1.0, 0.0); q = 1.0-p
        f = (b*p - q)/b if b>0 else 0.0; f = max(0.0, min(f, self.params.max_risk_pct))
        return round(self.params.bankroll * f, 2)
    def _place_back(self, market_id, selection_id, handicap, size, price, name: str):
        ORDERS_PLACED.labels(side="BACK").inc()
        write_event("order_placed", {"market_id": market_id, "selection_id": selection_id, "player": name, "side":"BACK", "size": size, "price": price})
        trade = Trade(market_id=market_id, selection_id=selection_id, handicap=handicap, strategy=self)
        order = trade.create_order(side="BACK", order_type=LimitOrder(price=price, size=size))
        self.flumine.place_order(order)
def tennis_market_filter(event_type_ids: List[str], inplay_only: bool, market_types: List[str]):
    return streaming_market_filter(event_type_ids=event_type_ids, market_types=market_types, turn_in_play_enabled=None, in_play_only=inplay_only)
def market_data_filter():
    return streaming_market_data_filter(fields=["EX_BEST_OFFERS_DISP", "EX_LTP"], ladder_levels=1)
