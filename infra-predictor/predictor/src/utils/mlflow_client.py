import mlflow, os
def setup_mlflow():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI","http://mlflow.mlflow.svc:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT","tennis-predictor"))
    return mlflow
