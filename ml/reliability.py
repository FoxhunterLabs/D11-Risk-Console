from typing import Dict
from core.utils import fclamp
from .config import MLRuntimeConfig

def per_sensor_reliability(per_anom: Dict[str, float], cfg: MLRuntimeConfig) -> Dict[str, float]:
    rel = {}
    for k, s in per_anom.items():
        r = cfg.max_reliability - s * (cfg.max_reliability - cfg.min_reliability)
        rel[k] = fclamp(r, cfg.min_reliability, cfg.max_reliability)
    return rel
