import math
import random
from typing import Dict, Any, Optional
from .rng import tick_rng
from core.config import SimConfig
from core.utils import fclamp

def _nrm(rng: random.Random, mu: float, sigma: float) -> float:
    u1 = max(1e-9, rng.random())
    u2 = max(1e-9, rng.random())
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mu + sigma * z

def generate_raw_tick(
    prev: Optional[Dict[str, Any]],
    *,
    seed: int,
    tick: int,
    cfg: SimConfig,
) -> Dict[str, Any]:
    rng = tick_rng(seed, tick, salt=11)

    if prev is None:
        state = {
            "speed_kph": 0.0,
            "gear": 1,
            "engine_rpm": 800,
            "grade_pct": 0.0,
            "roll_deg": 0.0,
            "pitch_deg": 0.0,
            "blade_load_pct": 0.0,
            "fuel_pct": 90.0,
            "ground_firmness": 0.7,
            "moisture_index": 0.3,
            "visibility": 0.9,
            "gnss_hdop": 0.8,
            "gnss_jitter_m": 0.3,
            "obstacle_distance_m": cfg.obstacle_none,
            "obstacle_bearing_deg": 0.0,
            "shift_hours": 2.0,
            "micro_corrections_per_min": 22.0,
        }
    else:
        state = dict(prev)

    state["shift_hours"] += 1 / 60

    target_speed = [2, 5, 8, 3][(tick // 40) % 4]
    state["speed_kph"] += _nrm(rng, (target_speed - state["speed_kph"]) * 0.25, 0.5)
    state["speed_kph"] = fclamp(state["speed_kph"], 0, cfg.max_speed_kph)

    state["gear"] = int(fclamp(round(1 + state["speed_kph"] / 3), 1, 4))
    state["engine_rpm"] = int(fclamp(800 + state["speed_kph"] * 120 + _nrm(rng, 0, 80), 800, 2100))

    state["grade_pct"] += _nrm(rng, 0, 0.5)
    state["grade_pct"] = fclamp(state["grade_pct"], -cfg.max_grade_pct, cfg.max_grade_pct)

    state["roll_deg"] += _nrm(rng, state["grade_pct"] * 0.03, 1.0)
    state["pitch_deg"] += _nrm(rng, state["grade_pct"] * 0.04, 0.8)
    state["roll_deg"] = fclamp(state["roll_deg"], -cfg.max_roll_deg, cfg.max_roll_deg)
    state["pitch_deg"] = fclamp(state["pitch_deg"], -cfg.max_pitch_deg, cfg.max_pitch_deg)

    if rng.random() < 0.06:
        state["obstacle_distance_m"] = rng.uniform(6, 35)
        state["obstacle_bearing_deg"] = rng.uniform(-120, 120)
    else:
        d = state["obstacle_distance_m"] + 3
        state["obstacle_distance_m"] = d if d <= cfg.obstacle_clip else cfg.obstacle_none

    state["tick"] = tick
    state["ts_label"] = f"D11_T{tick:06d}"
    return state
