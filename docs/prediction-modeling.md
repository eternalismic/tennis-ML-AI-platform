
# Prediction Modeling (Deeper Dive)

## Feature engineering
- **ELO & Surface ELO**: capture skill and surface specialization.
- **Recent form**: rolling win rates, last-N matches.
- **Head-to-head**: contextual indicator (small sample caution).
- **Context**: tournament level, round, fatigue proxies (rest days).

## Model families
- **Logistic regression**: baseline, interpretable, well-calibrated with Platt scaling.
- **Gradient boosting (e.g., XGBoost/LightGBM)**: handles nonlinearity & interactions.
- **Neural nets**: flexible; require careful regularization & data volume.

## Training loop
1. Split data (time-aware) into train/val/test.
2. Tune hyperparameters via cross-validation.
3. Fit model on training; early stop on validation.
4. Calibrate probabilities (Platt / isotonic) on validation.
5. Final evaluation on test (log loss, Brier, ROC-AUC, calibration curve).

## Probability calibration
A calibrated classifier outputs probabilities that match frequencies (buckets of 0.7 should win ~70%). Poor calibration impairs **edge detection** and **stake sizing**.

## Leakage & drift
- Avoid using post-match info or outcome-correlated stats.
- Monitor **concept drift** (seasonality, new players, injuries) and retrain.
