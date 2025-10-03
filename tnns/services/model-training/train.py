import os, mlflow, mlflow.pyfunc, pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, roc_auc_score

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI","http://mlflow:5000")
MLFLOW_S3_ENDPOINT_URL = os.getenv("MLFLOW_S3_ENDPOINT_URL","http://minio:9000")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID","minioadmin")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY","minioadmin")
MODEL_NAME = os.getenv("MODEL_NAME","tennis_win_predictor")

os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

rng = np.random.RandomState(42)
N = 2000
df = pd.DataFrame({
    "player_a": ["A"]*N,
    "player_b": ["B"]*N,
    "surface": rng.choice(["hard","clay","grass"], size=N),
    "round": rng.choice(["R1","QF","SF","F"], size=N),
    "elo_a": rng.normal(1600, 80, size=N),
    "elo_b": rng.normal(1600, 80, size=N),
    "h2h_a_over_b": rng.uniform(0,1,size=N),
    "form_a_10": rng.uniform(0,1,size=N),
    "form_b_10": rng.uniform(0,1,size=N),
})
logit = 0.01*(df["elo_a"]-df["elo_b"]) + 1.2*(df["form_a_10"]-df["form_b_10"]) + 0.5*(df["h2h_a_over_b"]-0.5)
p = 1/(1+np.exp(-logit))
y = (rng.uniform(0,1,size=N) < p).astype(int)

X = pd.get_dummies(df[["surface","round","elo_a","elo_b","h2h_a_over_b","form_a_10","form_b_10"]], drop_first=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
clf = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
pred_proba = clf.predict_proba(Xte)[:,1]
metrics = {"logloss": float(log_loss(yte, pred_proba)), "auc": float(roc_auc_score(yte, pred_proba))}

class ModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, columns):
        self.columns = columns
        self.clf = clf
    def predict(self, context, model_input):
        import pandas as pd, numpy as np
        df = model_input.copy()
        feats = pd.get_dummies(df[["surface","round","elo_a","elo_b","h2h_a_over_b","form_a_10","form_b_10"]], drop_first=True)
        for c in self.columns:
            if c not in feats: feats[c] = 0
        feats = feats[self.columns]
        prob_a = self.clf.predict_proba(feats)[:,1]
        return prob_a

with mlflow.start_run() as run:
    mlflow.log_metrics(metrics)
    sig = mlflow.models.signature.infer_signature(Xte, pred_proba)
    wrapper = ModelWrapper(X.columns.tolist())
    mlflow.pyfunc.log_model("model", python_model=wrapper, signature=sig)
    run_id = run.info.run_id
    uri = f"runs:/{run_id}/model"
    result = mlflow.register_model(uri, MODEL_NAME)
    print("Registered:", result.name, result.version)
