from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class TelemetryRow:
    tick: int
    ts_label: str

    speed_kph: float
    gear: int
    engine_rpm: int
    grade_pct: float
    roll_deg: float
    pitch_deg: float
    blade_load_pct: float
    fuel_pct: float

    ground_firmness: float
    moisture_index: float
    visibility: float

    gnss_hdop: float
    gnss_jitter_m: float
    obstacle_distance_m: float
    obstacle_bearing_deg: float

    shift_hours: float
    micro_corrections_per_min: float

    rollover_risk: float
    slip_risk: float
    obstacle_risk: float
    gnss_confidence: float
    overall_risk: float
    state: str

    overall_risk_with_ml: float = 0.0
    state_with_ml: str = "STABLE"


@dataclass
class Proposal:
    id: int
    created_ts: str
    title: str
    rationale: str
    status: str
    snapshot: Dict[str, Any]
