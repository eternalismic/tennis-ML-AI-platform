
# Evaluation & Calibration

## Proper scoring rules
- **Log loss (cross-entropy)** — penalizes overconfident wrong predictions.
- **Brier score** — mean squared error of probabilities.

## Ranking & discrimination
- **ROC-AUC**, **PR-AUC** — how well probabilities separate outcomes.

## Calibration
- Reliability diagrams; temperature scaling, Platt, isotonic.
- Calibrated probs → stable edges → consistent staking.

## Business metrics
- Expected value (EV) of bets, realized P/L, ROI, drawdown.
- Coverage (how often we bet) vs selectivity (edge threshold).
