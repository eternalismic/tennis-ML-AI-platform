
import logging, datetime
from typing import Optional, List, Dict
from dataclasses import dataclass
from flumine import BaseStrategy
from flumine.order.trade import Trade
from flumine.order.order import LimitOrder, OrderStatus
from betfairlightweight.filters import streaming_market_filter, streaming_market_data_filter
from betfairlightweight.resources import MarketBook
from .mcp import MCP, MarketContext
from .metrics import ORDERS_PLACED, ORDERS_MATCHED, EDGE_OBS, PENDING_EXPOSURE, PNL_TOTAL, ROI, BANKROLL, DAILY_BETS, DAILY_PNL

logger = logging.getLogger(__name__)

@dataclass
class StrategyParams:
    edge_threshold: float
    max_risk_pct: float
    bankroll: float
    min_odds: float
    max_odds: float
    daily_stop_loss: float
    daily_take_profit: float
    daily_max_bets: int

class MCPTennisStrategy(BaseStrategy):
    def __init__(self, mcp: MCP, params: StrategyParams, **kwargs):
        super().__init__(**kwargs)
        self.mcp = mcp
        self.params = params
        self.positions: Dict[str, list] = {}
        self.settled: Dict[str, bool] = {}
        self.total_staked = 0.0
        self._rollover_date = datetime.date.today()
        BANKROLL.set(self.params.bankroll)

    def _roll_daily(self):
        today = datetime.date.today()
        if today != self._rollover_date:
            self._rollover_date = today
            DAILY_BETS.set(0)
            DAILY_PNL.set(0)

    def check_market_book(self, market, market_book: MarketBook) -> bool:
        return market_book.status != "CLOSED"

    def _best_back(self, runner) -> Optional[float]:
        try:
            prices = runner.ex.available_to_back
            if prices:
                return prices[0]["price"]
        except Exception:
            return None
        return None

    def _circuit_breaker_open(self) -> bool:
        if DAILY_PNL._value.get() <= -abs(self.params.daily_stop_loss):
            return True
        if DAILY_PNL._value.get() >= abs(self.params.daily_take_profit):
            return True
        if DAILY_BETS._value.get() >= self.params.daily_max_bets:
            return True
        return False

    def process_market_book(self, market, market_book: MarketBook) -> None:
        try:
            self._roll_daily()
            if self._circuit_breaker_open():
                return
            runners = market_book.runners
            if len(runners) < 2:
                return
            rc = market.market_catalogue
            if not rc or not rc.runners or len(rc.runners) < 2:
                return
            nameA = rc.runners[0].runner_name
            nameB = rc.runners[1].runner_name
            selA = runners[0]; selB = runners[1]

            backA = self._best_back(selA)
            backB = self._best_back(selB)

            ctx = MarketContext(nameA, nameB, backA, None, backB, None, score=None, server=None)
            res = self.mcp.evaluate(ctx, edge_threshold=self.params.edge_threshold)

            if res.rec == "BACK_A" and backA and self.params.min_odds <= backA <= self.params.max_odds:
                stake = self._stake(res.model_prob_A, backA)
                if stake > 0:
                    self._place_back(market_book.market_id, selA.selection_id, selA.handicap, stake, backA)
                    EDGE_OBS.observe(res.edge)
                    self.total_staked += stake
                    DAILY_BETS.set(DAILY_BETS._value.get() + 1)
            elif res.rec == "BACK_B" and backB and self.params.min_odds <= backB <= self.params.max_odds:
                stake = self._stake(res.model_prob_B, backB)
                if stake > 0:
                    self._place_back(market_book.market_id, selB.selection_id, selB.handicap, stake, backB)
                    EDGE_OBS.observe(res.edge)
                    self.total_staked += stake
                    DAILY_BETS.set(DAILY_BETS._value.get() + 1)

            if market_book.status == "CLOSED" and not self.settled.get(market_book.market_id):
                self._settle_market(market_book)
                self.settled[market_book.market_id] = True
        except Exception as e:
            logger.exception("Error processing market_book: %s", e)

    def process_orders(self, market, orders: list) -> None:
        for order in orders:
            if order.size_matched and order.size_matched > 0:
                ORDERS_MATCHED.labels(side=str(order.side)).inc()
                md = {
                    "selection_id": order.selection_id,
                    "side": str(order.side),
                    "avg_price": float(order.average_price_matched) if order.average_price_matched else None,
                    "size": float(order.size_matched),
                }
                self.positions.setdefault(order.market_id, []).append(md)
        exposure = 0.0
        for order in orders:
            if order.status == OrderStatus.EXECUTABLE and order.size_remaining:
                try:
                    exposure += float(order.size_remaining) * float(order.order_type.price or 0.0)
                except Exception:
                    pass
        PENDING_EXPOSURE.set(exposure)

    def _settle_market(self, market_book: MarketBook):
        winner_ids = [r.selection_id for r in market_book.runners if getattr(r, "status", None) == "WINNER"]
        if not winner_ids:
            return
        winner = winner_ids[0]
        pnl = 0.0
        for md in self.positions.get(market_book.market_id, []):
            if md["side"].upper() == "BACK":
                if md["selection_id"] == winner:
                    pnl += (md["avg_price"] - 1.0) * md["size"]
                else:
                    pnl -= md["size"]
        PNL_TOTAL.set(PNL_TOTAL._value.get() + pnl)
        if self.total_staked > 0:
            ROI.set(PNL_TOTAL._value.get() / self.total_staked)

    def _stake(self, p: float, price: float) -> float:
        b = max(price - 1.0, 0.0)
        q = 1.0 - p
        f = (b * p - q) / b if b > 0 else 0.0
        f = max(0.0, min(f, self.params.max_risk_pct))
        stake = round(self.params.bankroll * f, 2)
        return stake

    def _place_back(self, market_id: str, selection_id: int, handicap: float, size: float, price: float):
        logger.info("Placing BACK order mkt=%s sel=%s size=%.2f @ %.2f", market_id, selection_id, size, price)
        ORDERS_PLACED.labels(side="BACK").inc()
        trade = Trade(market_id=market_id, selection_id=selection_id, handicap=handicap, strategy=self)
        order = trade.create_order(side="BACK", order_type=LimitOrder(price=price, size=size))
        self.flumine.place_order(order)

def tennis_market_filter(event_type_ids: List[str], inplay_only: bool, market_types: List[str]):
    return streaming_market_filter(event_type_ids=event_type_ids, market_types=market_types, turn_in_play_enabled=None, in_play_only=inplay_only)

def market_data_filter():
    return streaming_market_data_filter(fields=["EX_BEST_OFFERS_DISP", "EX_LTP"], ladder_levels=1)
