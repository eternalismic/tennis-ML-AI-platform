import argparse, os, joblib, boto3
from ..models.match_model import MatchOutcomeModel

def export_sklearn(model: MatchOutcomeModel, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(model.model, os.path.join(out_dir, "model.joblib"))
    with open(os.path.join(out_dir,"MLmodel"),"w") as f: f.write("# sklearn model exported for KServe\n")
    return out_dir

def upload_s3(local_dir: str, s3_uri: str):
    assert s3_uri.startswith("s3://")
    _, rest = s3_uri.split("s3://",1)
    bucket, key_prefix = rest.split("/",1) if "/" in rest else (rest,"")
    s3 = boto3.client("s3", endpoint_url=os.getenv("S3_ENDPOINT_URL"))
    for root, _, files in os.walk(local_dir):
        for name in files:
            p = os.path.join(root, name); rel = os.path.relpath(p, local_dir)
            key = f"{key_prefix.rstrip('/')}/{rel}"; s3.upload_file(p, bucket, key)
            print(f"[+] Uploaded s3://{bucket}/{key}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", default="kserve_export")
    ap.add_argument("--s3-uri", required=True)
    args = ap.parse_args()
    model = MatchOutcomeModel()
    export_dir = export_sklearn(model, args.artifact); upload_s3(export_dir, args.s3_uri)

if __name__=="__main__": main()
