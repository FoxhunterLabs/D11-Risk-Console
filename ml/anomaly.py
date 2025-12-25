import math
import numpy as np
from typing import Dict, Tuple, List
from .features import SENSOR_KEYS
from core.utils import fclamp

def robust_mad(values: np.ndarray) -> Tuple[float, float]:
    med = float(np.median(values))
    mad = float(np.median(np.abs(values - med)))
    return med, max(1e-6, 1.4826 * mad)

def anomaly_score(z: float) -> float:
    return 1.0 - math.exp(-abs(z) / 3.0)

def compute_anomaly(df, window: int) -> Tuple[float, Dict[str, float], List[str]]:
    if len(df) < window // 2:
        return 0.0, {}, ["insufficient_history"]

    tail = df.tail(window)
    per = {}
    reasons = []

    for k in SENSOR_KEYS:
        if k not in tail:
            continue
        series = tail[k].astype(float).to_numpy()
        med, mad = robust_mad(series)
        z = (float(df.iloc[-1][k]) - med) / mad
        s = fclamp(anomaly_score(z), 0, 1)
        per[k] = s

    top = sorted(per.values(), reverse=True)[:5]
    score = float(sum(top) / max(1, len(top)))
    return fclamp(score, 0, 1), per, reasons
