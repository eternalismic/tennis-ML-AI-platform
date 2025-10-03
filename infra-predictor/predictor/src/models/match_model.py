import numpy as np
from dataclasses import dataclass
from typing import Any, Dict, List
from sklearn.linear_model import LogisticRegression
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except Exception:
    HAS_XGB = False

@dataclass
class MatchOutcomeModel:
    model: Any = None
    feature_names: List[str] = None

    def __post_init__(self):
        if self.model is None:
            if HAS_XGB:
                self.model = XGBClassifier(
                    n_estimators=300, max_depth=4, learning_rate=0.05,
                    subsample=0.9, colsample_bytree=0.9, eval_metric="logloss", n_jobs=2
                )
            else:
                self.model = LogisticRegression(max_iter=500)

    def fit(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        self.feature_names = feature_names
        self.model.fit(X, y)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)[:,1]

    def features_from_row(self, row: Dict, elo_prob: float) -> np.ndarray:
        feats = [
            elo_prob,
            row.get("rank_a", 150), row.get("rank_b", 150),
            row.get("h2h_a_over_b", 0),
            1 if row.get("surface","hard")=="clay" else 0,
            1 if row.get("surface","hard")=="grass" else 0,
            row.get("recent_winrate_a", 0.5), row.get("recent_winrate_b", 0.5),
        ]
        return np.array(feats, dtype=float)
