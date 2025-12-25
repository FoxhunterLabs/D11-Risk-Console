import json
from pathlib import Path
from typing import Dict, Any, Tuple

MODELS_DIR = Path.cwd() / "models"
MODELS_DIR.mkdir(exist_ok=True)

REGISTRY_PATH = MODELS_DIR / "index.json"


def _default_registry() -> Dict[str, Any]:
    return {
        "active": None,
        "artifacts": {}
    }


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return _default_registry()
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return _default_registry()


def save_registry(reg: Dict[str, Any]) -> None:
    REGISTRY_PATH.write_text(
        json.dumps(reg, indent=2, sort_keys=True),
        encoding="utf-8"
    )


def upsert_artifact(name: str, meta: Dict[str, Any]) -> None:
    reg = load_registry()
    reg.setdefault("artifacts", {})
    reg["artifacts"][name] = meta

    if reg.get("active") is None:
        reg["active"] = name

    save_registry(reg)


def set_active(name: str) -> bool:
    reg = load_registry()
    if name not in reg.get("artifacts", {}):
        return False
    reg["active"] = name
    save_registry(reg)
    return True


def delete_artifact(name: str) -> Tuple[bool, str]:
    reg = load_registry()

    if reg.get("active") == name:
        return False, "Cannot delete active model"

    if name not in reg.get("artifacts", {}):
        return False, "Model not found"

    reg["artifacts"].pop(name, None)
    save_registry(reg)
    return True, "Deleted"


def prune_keep_last(n_keep: int = 8) -> Tuple[int, str]:
    reg = load_registry()
    artifacts = reg.get("artifacts", {})
    active = reg.get("active")

    if not artifacts:
        return 0, "Nothing to prune"

    def created_at(k: str):
        return artifacts.get(k, {}).get("created_at", "")

    names = sorted(artifacts.keys(), key=lambda k: created_at(k), reverse=True)

    keep = set(names[:n_keep])
    if active:
        keep.add(active)

    removed = 0
    for name in list(artifacts.keys()):
        if name not in keep:
            artifacts.pop(name, None)
            removed += 1

    save_registry(reg)
    return removed, f"Pruned {removed} model(s)"
