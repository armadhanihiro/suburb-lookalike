import json
import time
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("logs/search_log.jsonl")

LOG_PATH.parent.mkdir(exist_ok=True)


def log_search(
    reference,
    alpha,
    top_n,
    duration_ms,
    returned,
):
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "reference": reference,
        "alpha": alpha,
        "top_n": top_n,
        "duration_ms": round(duration_ms, 2),
        "returned": returned,
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record))
        f.write("\n")