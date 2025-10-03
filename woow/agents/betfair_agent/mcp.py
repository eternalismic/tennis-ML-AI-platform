
from dataclasses import dataclass
from typing import Optional, Tuple
import logging
import requests

logger = logging.getLogger(__name__)

def implied_probability(price: float) -> float:
    if price <= 0:
        return 0.0
    return 1.0 / price

@dataclass
class MCPResult:
    rec: str
    edge: float
    fair_odds_A: float
    fair_odds_B: float
    model_prob_A: float
    model_prob_B: float

class MarketContext:
    def __init__(self, playerA: str, playerB: str,
                 backA: Optional[float], layA: Optional[float],
                 backB: Optional[float], layB: Optional[float],
                 score: Optional[str] = None, server: Optional[str] = None):
        self.playerA = playerA; self.playerB = playerB
        self.backA = backA; self.layA = layA; self.backB = backB; self.layB = layB
        self.score = score; self.server = server

class MCP:
    def __init__(self, prediction_api_url: Optional[str] = None, prediction_api_key: Optional[str] = None):
        self.prediction_api_url = prediction_api_url
        self.prediction_api_key = prediction_api_key

    def _call_prediction_api(self, playerA: str, playerB: str, score: Optional[str]) -> Optional[Tuple[float, float]]:
        if not self.prediction_api_url:
            return None
        try:
            headers = {"Authorization": f"Bearer {self.prediction_api_key}"} if self.prediction_api_key else {}
            payload = {"player_a": playerA, "player_b": playerB, "score": score}
            resp = requests.post(self.prediction_api_url, json=payload, headers=headers, timeout=3)
            resp.raise_for_status()
            data = resp.json()
            pa = float(data.get("prob_a", 0.5)); pb = float(data.get("prob_b", 1.0 - pa))
            pa = max(0.0, min(1.0, pa)); pb = max(0.0, min(1.0, pb))
            s = pa + pb
            if s > 0 and abs(s-1.0) > 1e-6:
                pa, pb = pa/s, pb/s
            return pa, pb
        except Exception as e:
            logger.warning("Prediction API call failed: %s", e)
            return None

    def _baseline_model(self, backA: Optional[float], backB: Optional[float]) -> Tuple[float, float]:
        if backA and backB and backA > 0 and backB > 0:
            pa_mkt = implied_probability(backA); pb_mkt = implied_probability(backB)
            s = pa_mkt + pb_mkt
            if s > 0:
                return pa_mkt / s, pb_mkt / s
        return 0.5, 0.5

    def evaluate(self, ctx: MarketContext, edge_threshold: float = 0.05) -> MCPResult:
        from .metrics import MCP_EVALS, MCP_RECS
        MCP_EVALS.inc()
        model = self._call_prediction_api(ctx.playerA, ctx.playerB, ctx.score)
        if model is None:
            pa, pb = self._baseline_model(ctx.backA, ctx.backB)
        else:
            pa, pb = model

        fairA = 1.0 / max(pa, 1e-9); fairB = 1.0 / max(pb, 1e-9)

        edgeA = (ctx.backA - fairA) / fairA if ctx.backA else -1.0
        edgeB = (ctx.backB - fairB) / fairB if ctx.backB else -1.0

        rec = "NO_BET"; edge = 0.0
        if ctx.backA and edgeA >= edge_threshold:
            rec = "BACK_A"; edge = edgeA
        if ctx.backB and edgeB >= edge_threshold and (edgeB > edge):
            rec = "BACK_B"; edge = edgeB
        MCP_RECS.labels(rec=rec).inc()
        return MCPResult(rec=rec, edge=edge, fair_odds_A=fairA, fair_odds_B=fairB,
                         model_prob_A=pa, model_prob_B=pb)
