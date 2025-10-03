import argparse, pandas as pd
from sklearn.metrics import brier_score_loss, roc_auc_score, accuracy_score
from sklearn.calibration import calibration_curve
import json
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-csv", required=True)
    args = ap.parse_args()
    df = pd.read_csv(args.pred_csv)
    y, p = df['y_true'].values, df['p_pred'].values
    acc = accuracy_score(y, p>=0.5); brier=brier_score_loss(y,p); auc=roc_auc_score(y,p)
    frac_pos, mean_pred = calibration_curve(y,p,n_bins=10)
    print(json.dumps({"accuracy":float(acc),"brier":float(brier),"auc":float(auc),
                      "calibration":{"mean_pred":mean_pred.tolist(),"frac_pos":frac_pos.tolist()}}, indent=2))
if __name__=="__main__": main()
