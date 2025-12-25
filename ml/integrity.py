import json
import hashlib
import numpy as np
from typing import Dict, Any
from pathlib import Path


def _np_bytes(arr) -> bytes:
    a = np.asarray(arr, dtype=np.float64)
    return a.tobytes(order="C")


def _canonical_json(obj: Dict[str, Any]) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    ).encode("utf-8")


def compute_artifact_hash(*, meta: Dict[str, Any], scaler, pca, ridge) -> str:
    """
    REAL integrity hash:
      - metadata (minus artifact_hash itself)
      - scaler mean + scale
      - pca components + mean
      - ridge coef + intercept
    """
    meta_clean = dict(meta)
    meta_clean.pop("artifact_hash", None)

    parts = [
        b"D11_ARTIFACT_V1|",
        _canonical_json(meta_clean),
        b"|scaler_mean|", _np_bytes(getattr(scaler, "mean_", [])),
        b"|scaler_scale|", _np_bytes(getattr(scaler, "scale_", [])),
        b"|pca_components|", _np_bytes(getattr(pca, "components_", [])),
        b"|pca_mean|", _np_bytes(getattr(pca, "mean_", [])),
        b"|ridge_coef|", _np_bytes(getattr(ridge, "coef_", [])),
        b"|ridge_intercept|", _np_bytes(getattr(ridge, "intercept_", [])),
    ]

    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return h.hexdigest()


def sidecar_path(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta_sha256")
