from core.utils import fclamp
from .anomaly import compute_anomaly
from .ood import score_ood_uncertainty
from .reliability import per_sensor_reliability
from .config import MLRuntimeConfig

def compute_ml_overlay(df, cfg: MLRuntimeConfig, artifact):
    anomaly, per, reasons = compute_anomaly(df, cfg.window)
    ood, unc = score_ood_uncertainty(artifact, df)

    caution = 1.0 + 0.45 * anomaly + 0.35 * ood + 0.45 * unc
    caution = fclamp(caution, cfg.caution_mult_min, cfg.caution_mult_max)

    return {
        "anomaly": anomaly,
        "ood": ood,
        "uncertainty": unc,
        "per_sensor_reliability": per_sensor_reliability(per, cfg),
        "caution_mult": caution,
        "reasons": reasons,
    }
