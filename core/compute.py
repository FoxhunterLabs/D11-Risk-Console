from .risk import *
from .config import BaseWeights, SimConfig

def compute_full_row_from_raw(raw, *, weights: BaseWeights, cfg: SimConfig, gnss_weight_mult=1.0, caution_mult=1.0):
    rollover = compute_rollover_risk(raw["grade_pct"], raw["roll_deg"], raw["speed_kph"])
    slip = compute_slip_risk(raw["grade_pct"], raw["moisture_index"], raw["ground_firmness"], raw["speed_kph"])
    obstacle = compute_obstacle_risk(raw["obstacle_distance_m"], raw["speed_kph"], cfg)
    gnss_conf = compute_gnss_confidence(raw["gnss_hdop"], raw["gnss_jitter_m"], raw["visibility"])

    base_risk = compute_overall_risk(
        rollover, slip, obstacle, gnss_conf,
        weights=weights,
        gnss_weight_mult=gnss_weight_mult,
    )

    risk_ml = max(base_risk, base_risk * caution_mult)

    return {
        **raw,
        "rollover_risk": rollover,
        "slip_risk": slip,
        "obstacle_risk": obstacle,
        "gnss_confidence": gnss_conf,
        "overall_risk": base_risk,
        "state": classify_state(base_risk),
        "overall_risk_with_ml": risk_ml,
        "state_with_ml": classify_state(risk_ml),
    }
