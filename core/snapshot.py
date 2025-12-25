import json
from pathlib import Path
from typing import Any, Dict
from dataclasses import asdict
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_snapshot(
    *,
    reason: str,
    path: Path,
    session_contract: Dict[str, Any],
    seed: int,
    tick: int,
    running: bool,
    ml_enabled: bool,
    ml_disabled_reason: str | None,
    train_cfg_active: Dict[str, Any] | None,
    runtime_cfg: Dict[str, Any] | None,
    history: list,
    proposals: list,
    audit_entries: list,
):
    snap = {
        "generated_at_utc": utc_now_iso(),
        "reason": reason,
        "seed": seed,
        "tick": tick,
        "running": running,
        "ml_enabled": ml_enabled,
        "ml_disabled_reason": ml_disabled_reason,
        "session_contract": session_contract,
        "train_cfg_active": train_cfg_active,
        "runtime_cfg": runtime_cfg,
        "history": history,
        "proposals": proposals,
        "audit": audit_entries,
        "audit_head_hash": audit_entries[-1]["entry_hash"] if audit_entries else "GENESIS",
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(snap, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return path
