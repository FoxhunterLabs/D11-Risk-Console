from typing import List, Dict, Any
import pandas as pd
from core.config import SimConfig
from .raw_generator import generate_raw_tick

def replay_raw(
    *,
    seed: int,
    target_tick: int,
    cfg: SimConfig,
) -> pd.DataFrame:
    history: List[Dict[str, Any]] = []
    prev = None

    for t in range(1, target_tick + 1):
        raw = generate_raw_tick(prev, seed=seed, tick=t, cfg=cfg)
        history.append(raw)
        prev = raw

    return pd.DataFrame(history)
