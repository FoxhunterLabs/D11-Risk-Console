from dataclasses import dataclass

@dataclass(frozen=True)
class SimConfig:
    max_speed_kph: float = 12.0
    max_grade_pct: float = 22.0
    max_roll_deg: float = 18.0
    max_pitch_deg: float = 15.0
    obstacle_none: float = 999.0
    obstacle_clip: float = 80.0


@dataclass
class BaseWeights:
    rollover: float = 0.38
    slip: float = 0.34
    obstacle: float = 0.28
    gnss_penalty: float = 0.25
