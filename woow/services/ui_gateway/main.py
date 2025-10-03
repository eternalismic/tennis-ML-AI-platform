
import os, asyncio, json, time, requests
from fastapi import FastAPI, Response, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from typing import Optional, Dict, Any
from jose import jwt

app = FastAPI(title="UI Gateway", version="0.3.0")
EVENTS_PATH = os.getenv("AGENT_EVENTS_PATH", "/var/log/agent/events.jsonl")
PROM_URL = os.getenv("PROM_URL", "http://prometheus-k8s.monitoring:9090")
PROM_BEARER = os.getenv("PROM_BEARER", "")
OIDC_ISSUER = os.getenv("OIDC_ISSUER_URL", "").rstrip("/")
OIDC_AUDIENCE = os.getenv("OIDC_AUDIENCE", "")
OIDC_JWKS_URL = os.getenv("OIDC_JWKS_URL", "")
_jwks_cache = {"ts":0, "jwks":None}

def _jwks():
    import requests, time
    now=time.time()
    global _jwks_cache
    if _jwks_cache["jwks"] and now-_jwks_cache["ts"]<600: return _jwks_cache["jwks"]
    url = OIDC_JWKS_URL
    if not url and OIDC_ISSUER:
        try: url = requests.get(f"{OIDC_ISSUER}/.well-known/openid-configuration", timeout=3).json().get("jwks_uri")
        except Exception: url=None
    if not url: return None
    r=requests.get(url, timeout=3); r.raise_for_status()
    _jwks_cache={"ts":now,"jwks":r.json()}; return _jwks_cache["jwks"]

def _verify_token(token: str) -> Dict[str, Any]:
    if not OIDC_ISSUER: return {"sub":"dev-user"}
    try:
        jwks=_jwks()
        if not jwks: raise HTTPException(status_code=503, detail="JWKS unavailable")
        unverified = jwt.get_unverified_header(token); kid = unverified.get("kid")
        key=None
        for k in jwks.get("keys", []):
            if k.get("kid")==kid: key=k; break
        if not key and jwks.get("keys"): key=jwks["keys"][0]
        claims = jwt.decode(token, key, algorithms=[key.get("alg","RS256")], audience=OIDC_AUDIENCE, issuer=OIDC_ISSUER)
        return claims
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

def _get_token(req: Request):
    auth=req.headers.get("Authorization","")
    if auth.startswith("Bearer "): return auth.split(" ",1)[1].strip()
    q=req.query_params.get("access_token"); return q

async def guard(req: Request):
    tok=_get_token(req)
    if tok is None:
        if not OIDC_ISSUER: return {"sub":"dev-user"}
        raise HTTPException(status_code=401, detail="Missing bearer token")
    return _verify_token(tok)

@app.get("/healthz")
def healthz(): return {"status":"ok"}

@app.get("/api/snapshot")
def snapshot():
    items=[]
    try:
        with open(EVENTS_PATH,"r",encoding="utf-8") as f:
            lines=f.readlines()[-100:]
        for line in lines:
            line=line.strip()
            if not line: continue
            items.append(json.loads(line))
    except FileNotFoundError:
        pass
    return {"events":items}

@app.get("/api/events")
async def events(_claims=Depends(guard)):
    async def event_stream():
        last_size=0
        while True:
            try:
                size=os.path.getsize(EVENTS_PATH)
                if size<last_size: last_size=0
                if size>last_size:
                    with open(EVENTS_PATH,"r",encoding="utf-8") as f:
                        f.seek(last_size); chunk=f.read(); last_size=size
                        for line in chunk.splitlines():
                            line=line.strip()
                            if not line: continue
                            yield f"data: {line}\n\n"
                await asyncio.sleep(0.5)
            except FileNotFoundError:
                await asyncio.sleep(1)
    return StreamingResponse(event_stream(), media_type="text/event-stream")

def _kelly(bankroll: float, p: float, price: float, max_risk_pct: float) -> float:
    b=max(price-1.0,0.0); q=1.0-p; f=(b*p-q)/b if b>0 else 0.0
    if f<0: f=0.0
    if f>max_risk_pct: f=max_risk_pct
    return round(bankroll*f,2)

@app.post("/simulate")
def simulate(body: Dict[str, Any], _claims=Depends(guard)):
    edge_th=float(body.get("edgeThreshold",0.05))
    max_risk_pct=float(body.get("maxRiskPct",0.01))
    bankroll=float(body.get("bankroll",1000.0))
    limit=int(body.get("limit",25))
    events=[]
    try:
        with open(EVENTS_PATH,"r",encoding="utf-8") as f:
            lines=f.readlines()[-500:]
        for line in lines:
            line=line.strip()
            if not line: continue
            ev=json.loads(line)
            if ev.get("kind")=="mcp_evaluation": events.append(ev)
    except FileNotFoundError:
        pass
    previews=[]
    for ev in events[-limit:]:
        p=ev["payload"]
        backA, backB = p.get("backA"), p.get("backB")
        pa, pb = p["probs"]["A"], p["probs"]["B"]
        fairA, fairB = p["fair_odds"]["A"], p["fair_odds"]["B"]
        edgeA = ((backA - fairA)/fairA) if backA else -1.0
        edgeB = ((backB - fairB)/fairB) if backB else -1.0
        rec="NO_BET"; stake=0.0; price=None; side_player=None
        if backA and edgeA>=edge_th and (edgeA>=edgeB):
            rec="BACK_A"; price=backA; stake=_kelly(bankroll, pa, backA, max_risk_pct); side_player=p["players"][0]
        elif backB and edgeB>=edge_th:
            rec="BACK_B"; price=backB; stake=_kelly(bankroll, pb, backB, max_risk_pct); side_player=p["players"][1]
        previews.append({"ts":ev["ts"],"players":p["players"],"edgeA":edgeA,"edgeB":edgeB,"rec":rec,"stake":stake,"price":price,"player":side_player})
    return {"count":len(previews),"edgeThreshold":edge_th,"maxRiskPct":max_risk_pct,"bankroll":bankroll,"previews":previews}

def _q(q: str):
    try:
        headers={"Accept":"application/json"}
        if PROM_BEARER: headers["Authorization"]=f"Bearer {PROM_BEARER}"
        r=requests.get(f"{PROM_URL}/api/v1/query", params={"query":q}, headers=headers, timeout=3)
        r.raise_for_status(); data=r.json(); res=data.get("data",{}).get("result",[])
        if not res: return None
        return float(res[0]["value"][1])
    except Exception: return None

@app.get("/api/metrics_summary")
def metrics_summary(_claims=Depends(guard)):
    pnl=_q("pnl_total"); roi=_q("roi_total"); orders=_q("sum(orders_placed_total)")
    by_side=None
    try:
        headers={"Accept":"application/json"}
        if PROM_BEARER: headers["Authorization"]=f"Bearer {PROM_BEARER}"
        r=requests.get(f"{PROM_URL}/api/v1/query", params={"query":"sum by (side) (orders_placed_total)"}, headers=headers, timeout=3)
        r.raise_for_status()
        res={}
        for it in r.json().get("data",{}).get("result",[]):
            side=it.get("metric",{}).get("side","unknown"); val=float(it["value"][1]); res[side]=val
        by_side=res
    except Exception:
        by_side=None
    return {"pnl_total":pnl,"roi_total":roi,"orders_placed_total":orders,"orders_by_side":by_side}
