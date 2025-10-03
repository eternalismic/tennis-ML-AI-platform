import os
from typing import Optional, Any, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response, JSONResponse

PRED_COUNT = Counter("predictions_total", "Number of predictions served")
app = FastAPI(title="Prediction API", version="0.3.0")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME")
MLFLOW_MODEL_STAGE = os.getenv("MLFLOW_MODEL_STAGE", "Production")

_model = None
_model_loaded_from_mlflow = False
_model_info: Dict[str, Any] = {}

def _load_mlflow_model():
    global _model, _model_loaded_from_mlflow, _model_info
    if not (MLFLOW_TRACKING_URI and MLFLOW_MODEL_NAME):
        _model = None
        _model_loaded_from_mlflow = False
        _model_info = {"loaded": False, "reason": "MLFLOW env not set"}
        return
    try:
        import mlflow
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model_uri = f"models:/{MLFLOW_MODEL_NAME}/{MLFLOW_MODEL_STAGE}"
        _model = mlflow.pyfunc.load_model(model_uri)
        _model_loaded_from_mlflow = True
        _model_info = {"loaded": True, "uri": model_uri}
    except Exception as e:
        _model = None
        _model_loaded_from_mlflow = False
        _model_info = {"loaded": False, "error": str(e)}

_load_mlflow_model()

class PredictRequest(BaseModel):
    player_a: str
    player_b: str
    context: Optional[dict] = None

@app.get("/health")
def health():
    return {"status": "ok", "mlflow": _model_info}

@app.post("/predict")
def predict(req: PredictRequest):
    PRED_COUNT.inc()
    if _model_loaded_from_mlflow and _model is not None:
        try:
            import pandas as pd
            payload = {"player_a": [req.player_a], "player_b": [req.player_b]}
            if req.context:
                for k, v in req.context.items():
                    payload[k] = [v]
            df = pd.DataFrame(payload)
            y = _model.predict(df)
            if hasattr(y, "tolist"):
                y = y.tolist()
            if isinstance(y, list) and len(y) == 1:
                y = y[0]
            prob_a = None
            prob_b = None
            if isinstance(y, dict):
                prob_a = float(y.get("prob_a", 0.5))
                prob_b = float(y.get("prob_b", 1.0 - prob_a))
            elif isinstance(y, (float, int)):
                prob_a = float(y)
                prob_b = 1.0 - prob_a
            elif isinstance(y, (list, tuple)) and len(y) == 2:
                prob_a = float(y[0])
                prob_b = float(y[1])
            else:
                prob_a = 0.5
                prob_b = 0.5
            prob_a = max(0.0, min(1.0, prob_a))
            prob_b = 1.0 - prob_a
            return {
                "player_a": req.player_a,
                "player_b": req.player_b,
                "probabilities": {"a": prob_a, "b": prob_b},
                "model": "mlflow",
                "mlflow": _model_info,
            }
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": "mlflow_predict_failed", "detail": str(e)})
    return {
        "player_a": req.player_a,
        "player_b": req.player_b,
        "probabilities": {"a": 0.63, "b": 0.37},
        "model": "placeholder",
        "mlflow": _model_info,
    }

@app.post("/reload-model")
def reload_model():
    _load_mlflow_model()
    return {"reloaded": True, "mlflow": _model_info}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
