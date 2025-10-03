# Pipelines
- Train: `src/pipeline/train.py` → MLflow metrics + predictions CSV.
- Evaluate: `src/pipeline/evaluate.py`.
- Calibration: `src/pipeline/calibration_report.py` → JSON + PNG (Airflow weekly).
- Promotion: `src/pipeline/promote_and_update_gitops.py` → MLflow staging→prod + GitOps values update (manual Airflow).
- Export for KServe: `src/pipeline/export_kserve.py` (uploads model.joblib to MinIO S3).
