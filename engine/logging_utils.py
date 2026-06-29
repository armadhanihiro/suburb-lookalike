import json
import time
from datetime import datetime
from pathlib import Path


LOG_PATH = Path("logs/search_log.jsonl")


def now_ms():
    return time.perf_counter()


def elapsed_ms(start_time):
    return round((time.perf_counter() - start_time) * 1000, 2)


def log_search(user_id, reference, alpha, top_n, preset, data_source, duration_ms, results):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_id": user_id,
        "reference": reference,
        "alpha": alpha,
        "top_n": top_n,
        "preset": preset,
        "data_source": data_source,
        "duration_ms": duration_ms,
        "results": results,
    }

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False))
        file.write("\n")