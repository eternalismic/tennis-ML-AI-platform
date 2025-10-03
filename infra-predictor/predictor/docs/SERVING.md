# Serving with KServe
1) Export: `python -m src.pipeline.export_kserve --s3-uri s3://mlflow-artifacts/models/tennis-outcome-sklearn/v1/`
2) Update ISVC `storageUri` and sync `kserve-isvc` Argo app. KServe downloads artifact from MinIO.
