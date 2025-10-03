import os, requests
BASE = os.getenv("LIVE_API_BASE","https://api.example.com")
KEY  = os.getenv("LIVE_API_KEY","")
def get_match_timeline(match_id: str):
    r = requests.get(f"{BASE}/v1/matches/{match_id}/timeline", params={"api_key":KEY}, timeout=10)
    r.raise_for_status()
    return r.json()
