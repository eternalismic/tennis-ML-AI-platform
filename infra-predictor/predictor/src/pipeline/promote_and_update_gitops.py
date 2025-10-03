import os, subprocess, tempfile, mlflow
def run(cmd, cwd=None, env=None):
    print("+", " ".join(cmd)); subprocess.check_call(cmd, cwd=cwd, env=env)
def main():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI","http://mlflow.mlflow.svc:5000"))
    model_name = os.getenv("MLFLOW_MODEL_NAME","tennis-outcome-xgb")
    client = mlflow.tracking.MlflowClient()
    latest = client.get_latest_versions(model_name, stages=["Staging"])
    if not latest: print("No staging model found"); return
    v = latest[0].version; print("Promoting version", v)
    client.transition_model_version_stage(model_name, v, stage="Production", archive_existing_versions=True)
    repo = os.environ["GITOPS_REPO_URL"]; branch = os.getenv("GITOPS_REPO_BRANCH","main")
    with tempfile.TemporaryDirectory() as td:
        env = os.environ.copy()
        if "GITOPS_SSH_KEY" in env:
            key_path = os.path.join(td,"id_ed25519"); open(key_path,"w").write(env["GITOPS_SSH_KEY"]); os.chmod(key_path,0o600)
            env["GIT_SSH_COMMAND"] = f"ssh -i {key_path} -o StrictHostKeyChecking=no"
        run(["git","clone","-b",branch,repo,td], env=env)
        values_path = os.path.join(td,"helm-charts","tennis-predictor","values.yaml")
        with open(values_path,"a") as f: f.write(f"\n# updated by promote_and_update_gitops.py\nmodelVersion: {v}\n")
        run(["git","add","-A"], cwd=td, env=env); run(["git","commit","-m",f"Promote {model_name} v{v}"], cwd=td, env=env); run(["git","push"], cwd=td, env=env)
if __name__ == "__main__": main()
