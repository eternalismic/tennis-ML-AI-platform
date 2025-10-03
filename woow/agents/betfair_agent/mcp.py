
from dataclasses import dataclass
from typing import Optional, Tuple
import logging, requests
logger = logging.getLogger(__name__)
def implied_probability(price: float) -> float:
    if price and price > 0: return 1.0/price
    return 0.0
@dataclass
class MCPResult:
    rec: str; edge: float; fair_odds_A: float; fair_odds_B: float; model_prob_A: float; model_prob_B: float
class MarketContext:
    def __init__(self, playerA, playerB, backA, layA, backB, layB, score=None, server=None):
        self.playerA, self.playerB = playerA, playerB
        self.backA, self.layA, self.backB, self.layB = backA, layA, backB, layB
        self.score, self.server = score, server
class MCP:
    def __init__(self, prediction_api_url: Optional[str] = None, prediction_api_key: Optional[str] = None):
        self.prediction_api_url = prediction_api_url; self.prediction_api_key = prediction_api_key
    def _call_prediction_api(self, playerA: str, playerB: str, score: Optional[str]):
        if not self.prediction_api_url: return None
        try:
            headers = {"Authorization": f"Bearer {self.prediction_api_key}"} if self.prediction_api_key else {}
            resp = requests.post(self.prediction_api_url, json={"player_a":playerA,"player_b":playerB,"score":score},
                                 headers=headers, timeout=3)
            resp.raise_for_status(); data = resp.json()
            pa = float(data.get("prob_a", 0.5)); pb = float(data.get("prob_b", 1.0-pa))
            s = pa+pb; 
            if s>0 and abs(s-1.0)>1e-6: pa, pb = pa/s, pb/s
            pa = max(0.0, min(1.0, pa)); pb = max(0.0, min(1.0, pb))
            return pa, pb
        except Exception as e:
            logger.warning("Prediction API call failed: %s", e); return None
    def _baseline_model(self, backA, backB):
        if backA and backB and backA>0 and backB>0:
            pa, pb = implied_probability(backA), implied_probability(backB); s=pa+pb
            if s>0: return pa/s, pb/s
        return 0.5, 0.5
    def evaluate(self, ctx: MarketContext, edge_threshold: float = 0.05) -> MCPResult:
        from .metrics import MCP_EVALS, MCP_RECS
        MCP_EVALS.inc()
        m = self._call_prediction_api(ctx.playerA, ctx.playerB, ctx.score)
        pa, pb = m if m else self._baseline_model(ctx.backA, ctx.backB)
        fairA, fairB = 1.0/max(pa,1e-9), 1.0/max(pb,1e-9)
        edgeA = ((ctx.backA - fairA)/fairA) if ctx.backA else -1.0
        edgeB = ((ctx.backB - fairB)/fairB) if ctx.backB else -1.0
        rec, edge = "NO_BET", 0.0
        if ctx.backA and edgeA >= edge_threshold: rec, edge = "BACK_A", edgeA
        if ctx.backB and edgeB >= edge_threshold and edgeB>edge: rec, edge = "BACK_B", edgeB
        MCP_RECS.labels(rec=rec).inc()
        return MCPResult(rec, edge, fairA, fairB, pa, pb)
