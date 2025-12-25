from .utils import fclamp
from .config import SimConfig, BaseWeights

def compute_rollover_risk(grade_pct, roll_deg, speed_kph):
    return fclamp(
        55 * abs(roll_deg) / 20
        + 30 * abs(grade_pct) / 25
        + 25 * speed_kph / 12,
        0, 100
    )

def compute_slip_risk(grade_pct, moisture, firmness, speed_kph):
    downhill = max(0.0, grade_pct / 20)
    return fclamp(
        40 * downhill
        + 35 * moisture
        + 35 * (1 - firmness)
        + 20 * speed_kph / 10,
        0, 100
    )

def compute_gnss_confidence(hdop, jitter, visibility):
    return fclamp(
        (
            0.45 * max(0, (3.5 - hdop) / 3.5)
            + 0.35 * max(0, (3.0 - jitter) / 3.0)
            + 0.20 * visibility
        ) * 100,
        0, 100
    )

def compute_obstacle_risk(distance_m, speed_kph, cfg: SimConfig):
    if distance_m >= cfg.obstacle_clip or distance_m == cfg.obstacle_none:
        return 0.0
    speed_mps = max(speed_kph / 3.6, 0.1)
    ttc = distance_m / speed_mps
    if ttc > 40:
        return 10
    if ttc > 20:
        return 35
    if ttc > 10:
        return 60
    return 85

def compute_overall_risk(
    rollover, slip, obstacle, gnss_conf, *,
    weights: BaseWeights,
    gnss_weight_mult: float = 1.0
):
    gnss_penalty = (100 - gnss_conf) * weights.gnss_penalty * gnss_weight_mult
    return fclamp(
        weights.rollover * rollover
        + weights.slip * slip
        + weights.obstacle * obstacle
        + gnss_penalty,
        0, 100
    )

def classify_state(risk):
    if risk < 25:
        return "STABLE"
    if risk < 50:
        return "ELEVATED"
    if risk < 75:
        return "HIGH"
    return "CRITICAL"
