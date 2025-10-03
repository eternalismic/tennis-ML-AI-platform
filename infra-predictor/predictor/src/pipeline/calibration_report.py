import argparse, pandas as pd, numpy as np, json
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, roc_auc_score, accuracy_score
import matplotlib.pyplot as plt
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-csv", required=True)
    ap.add_argument("--out-json", default="calibration.json")
    ap.add_argument("--out-png", default="calibration.png")
    args = ap.parse_args()
    df = pd.read_csv(args.pred_csv)
    y, p = df['y_true'].values, df['p_pred'].values
    acc = accuracy_score(y, p>=0.5); brier=brier_score_loss(y,p); auc=roc_auc_score(y,p)
    frac_pos, mean_pred = calibration_curve(y,p,n_bins=10)
    with open(args.out_json,"w") as f:
        json.dump({"accuracy":float(acc),"brier":float(brier),"auc":float(auc),
                   "calibration":{"mean_pred":mean_pred.tolist(),"frac_pos":frac_pos.tolist()}}, f, indent=2)
    plt.figure(); plt.plot(mean_pred, frac_pos, marker="o"); plt.plot([0,1],[0,1],"--")
    plt.xlabel("Predicted probability"); plt.ylabel("Fraction of positives"); plt.title("Calibration Curve")
    plt.savefig(args.out_png, bbox_inches="tight"); print(f"Wrote {args.out_json} and {args.out_png}")
if __name__=="__main__": main()
