from dataclasses import dataclass

@dataclass
class MLRuntimeConfig:
    enabled: bool = True

    anomaly_flag: float = 0.70
    ood_flag: float = 0.65
    uncertainty_flag: float = 0.65

    min_reliability: float = 0.60
    max_reliability: float = 1.00

    caution_mult_min: float = 1.00
    caution_mult_max: float = 1.30

    gnss_weight_mult_min: float = 1.00
    gnss_weight_mult_max: float = 1.20

    window: int = 60
