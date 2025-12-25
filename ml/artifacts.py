from pathlib import Path
from joblib import dump, load

from .integrity import compute_artifact_hash, sidecar_path


def save_artifact(artifact: dict, path: Path):
    """
    Saves artifact + integrity sidecar.
    """
    dump(artifact, path)

    meta = artifact.get("meta", {})
    scaler = artifact["scaler"]
    pca = artifact["pca"]
    ridge = artifact["ridge"]

    h = compute_artifact_hash(
        meta=meta,
        scaler=scaler,
        pca=pca,
        ridge=ridge,
    )

    meta["artifact_hash"] = h
    sidecar_path(path).write_text(h, encoding="utf-8")


def load_artifact_verified(path: Path) -> dict:
    """
    Load-time behavior:
      - missing sidecar → raise
      - hash mismatch → raise
    Caller decides how to disable ML.
    """
    artifact = load(path)
    meta = artifact.get("meta", {})

    scaler = artifact["scaler"]
    pca = artifact["pca"]
    ridge = artifact["ridge"]

    sidecar = sidecar_path(path)
    if not sidecar.exists():
        raise RuntimeError("missing_artifact_sidecar")

    expected = sidecar.read_text(encoding="utf-8").strip()
    actual = compute_artifact_hash(
        meta=meta,
        scaler=scaler,
        pca=pca,
        ridge=ridge,
    )

    if expected != actual or not expected:
        raise RuntimeError("artifact_hash_mismatch")

    return artifact
