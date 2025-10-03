import argparse, pandas as pd, numpy as np, mlflow, os, json
from ..models.elo import EloModel
from ..models.match_model import MatchOutcomeModel

def load_data(csv_path: str): return pd.read_csv(csv_path)

def build_features(df: pd.DataFrame, elo: EloModel):
    X=[]; y=[]
    for _,row in df.iterrows():
        a=row['player_a']; b=row['player_b']; surface=row.get('surface',None)
        p_elo = elo.prob_win(a,b,surface)
        y.append(1 if row['winner']==a else 0)
        f = [p_elo, row.get('rank_a',150), row.get('rank_b',150),
             row.get('h2h_a_over_b',0), 1 if row.get('surface','hard')=='clay' else 0,
             1 if row.get('surface','hard')=='grass' else 0,
             row.get('recent_winrate_a',0.5), row.get('recent_winrate_b',0.5)]
        X.append(f)
    feat = ['elo_prob','rank_a','rank_b','h2h','is_clay','is_grass','recent_wr_a','recent_wr_b']
    return np.array(X,float), np.array(y,int), feat

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--mlflow-uri", default=os.getenv("MLFLOW_TRACKING_URI","http://mlflow.mlflow.svc:5000"))
    ap.add_argument("--experiment", default="tennis-predictor")
    ap.add_argument("--output", default="model_preds.csv")
    args = ap.parse_args()

    mlflow.set_tracking_uri(args.mlflow_uri); mlflow.set_experiment(args.experiment)
    df = load_data(args.csv)
    elo = EloModel()
    for _,row in df.iterrows():
        w=row['winner']; l=row['player_b'] if w==row['player_a'] else row['player_a']
        elo.update(w,l,row.get('surface',None))
    X,y,feat = build_features(df, elo)
    model = MatchOutcomeModel()
    with mlflow.start_run():
        model.fit(X,y,feat)
        from sklearn.metrics import brier_score_loss, log_loss, accuracy_score
        p = model.predict_proba(X)
        mlflow.log_metric("acc", float(accuracy_score(y,p>=0.5)))
        mlflow.log_metric("brier", float(brier_score_loss(y,p)))
        mlflow.log_metric("logloss", float(log_loss(y,p)))
        mlflow.log_param("features", json.dumps(feat))
        out = pd.DataFrame({"y_true":y,"p_pred":p})
        out.to_csv(args.output, index=False)
        mlflow.log_artifact(args.output)

if __name__=="__main__": main()
