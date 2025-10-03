
import json, os, time, threading
from typing import Any, Dict
DEFAULT_PATH = os.getenv("AGENT_EVENTS_PATH", "/var/log/agent/events.jsonl")
os.makedirs(os.path.dirname(DEFAULT_PATH), exist_ok=True)
_lock = threading.Lock()
def write_event(kind: str, payload: Dict[str, Any], path: str = DEFAULT_PATH) -> None:
    ev = { "ts": time.time(), "kind": kind, "payload": payload }
    line = json.dumps(ev, ensure_ascii=False)
    with _lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
