from typing import Any
from datetime import datetime, timezone

CANON_FLOAT_DIGITS = 6

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def fclamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def canonicalize(x: Any) -> Any:
    if isinstance(x, float):
        return round(x, CANON_FLOAT_DIGITS)
    if isinstance(x, dict):
        return {k: canonicalize(x[k]) for k in sorted(x.keys())}
    if isinstance(x, list):
        return [canonicalize(v) for v in x]
    return x
