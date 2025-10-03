from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
import time

from ..models.elo import EloModel
from ..models.markov import match_win_prob, set_win_prob

app = FastAPI(title="Tennis Predictor", version="0.4.0")
# Endpoint-level
REQ = Counter("predict_requests_total","Requests",["endpoint"])
LAT = Histogram("predict_latency_seconds","Latency",["endpoint"])
# HTTP-level
HTTP_REQS = Counter("http_requests_total","HTTP requests",["status","path"])
HTTP_LAT  = Histogram("http_request_duration_seconds","HTTP request duration",[ "path" ])

@app.middleware("http")
async def prometheus_mw(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    dur = time.perf_counter()-start
    path = request.url.path
    status = str(response.status_code)
    HTTP_REQS.labels(status, path).inc()
    HTTP_LAT.labels(path).observe(dur)
    return response

elo = EloModel()

class PreMatchInput(BaseModel):
    player_a: str
    player_b: str
    surface: str|None = None
    best_of: int = 3
    rank_a: int|None = None
    rank_b: int|None = None

class LiveInput(BaseModel):
    player_a: str
    player_b: str
    server: str = "A"
    set_score: tuple[int,int] = (0,0)
    game_score: tuple[int,int] = (0,0)
    p_hold_a: float | None = None
    p_hold_b: float | None = None
    best_of: int = 3

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/metrics")
def metrics(): return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict/prematch")
def predict_prematch(inp: PreMatchInput):
    REQ.labels("prematch").inc()
    with LAT.labels("prematch").time():
        p_elo = elo.prob_win(inp.player_a, inp.player_b, inp.surface)
        p_hold_a = 0.6 + 0.3*(p_elo - 0.5)
        p_hold_b = 0.6 - 0.3*(p_elo - 0.5)
        p_match = match_win_prob(p_hold_a, p_hold_b, inp.best_of)
        return {"player_a": inp.player_a, "player_b": inp.player_b, "prob_win_a": p_match, "elo_prob": p_elo}

@app.post("/predict/live")
def predict_live(inp: LiveInput):
    REQ.labels("live").inc()
    with LAT.labels("live").time():
        p_elo = elo.prob_win(inp.player_a, inp.player_b, None)
        p_hold_a = inp.p_hold_a or (0.6 + 0.3*(p_elo - 0.5))
        p_hold_b = inp.p_hold_b or (0.6 - 0.3*(p_elo - 0.5))
        p_set = set_win_prob(p_hold_a, p_hold_b, "A" if inp.server=="A" else "B")
        p_match = match_win_prob(p_hold_a, p_hold_b, inp.best_of)
        return {"p_set_a": p_set, "p_match_a": p_match, "p_hold_a": p_hold_a, "p_hold_b": p_hold_b, "elo_prob": p_elo}
