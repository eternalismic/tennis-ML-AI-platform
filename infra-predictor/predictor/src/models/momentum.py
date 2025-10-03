import numpy as np
from dataclasses import dataclass
from typing import Any, List, Dict
from sklearn.ensemble import GradientBoostingClassifier
try:
    from xgboost import XGBClassifier
    HAS_XGB=True
except Exception:
    HAS_XGB=False

@dataclass
class MomentumModel:
    model: Any = None
    features: List[str] = None

    def __post_init__(self):
        self.model = XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9) if HAS_XGB else GradientBoostingClassifier()

    def fit(self, X: np.ndarray, y: np.ndarray, features: List[str]):
        self.features = features
        self.model.fit(X,y)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)[:,1]

    def features_from_state(self, s: Dict) -> np.ndarray:
        feats = [
            s.get("streak_a",0), s.get("streak_b",0),
            s.get("aces_a",0), s.get("aces_b",0),
            s.get("df_a",0), s.get("df_b",0),
            s.get("first_serve_pct_a",0.6), s.get("first_serve_pct_b",0.6),
        ]
        return np.array(feats, dtype=float)
