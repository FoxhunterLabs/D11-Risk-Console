import json
import hashlib
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, Deque
from collections import deque

from .utils import canonicalize


def sha256_json(obj: Any) -> str:
    payload = json.dumps(
        canonicalize(obj),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass
class AuditEntry:
    ts: str
    kind: str
    summary: str
    meta: Dict[str, Any] = field(default_factory=dict)
    prev_hash: str = "GENESIS"
    entry_hash: str = ""


class AuditChain:
    def __init__(self, maxlen: int = 600):
        self._log: Deque[AuditEntry] = deque(maxlen=maxlen)

    @property
    def head_hash(self) -> str:
        if not self._log:
            return "GENESIS"
        return self._log[-1].entry_hash

    def append(self, *, ts: str, kind: str, summary: str, meta: Optional[Dict[str, Any]] = None):
        meta = meta or {}
        prev = self.head_hash

        payload = {
            "ts": ts,
            "kind": kind,
            "summary": summary,
            "meta": meta,
            "prev_hash": prev,
        }

        h = sha256_json(payload)

        self._log.append(
            AuditEntry(
                ts=ts,
                kind=kind,
                summary=summary,
                meta=meta,
                prev_hash=prev,
                entry_hash=h,
            )
        )

    def entries(self):
        return list(self._log)

    def to_json(self) -> str:
        return json.dumps(
            [asdict(e) for e in self._log],
            indent=2,
            sort_keys=True,
        )

    def to_csv_rows(self):
        rows = []
        for e in self._log:
            rows.append({
                "ts": e.ts,
                "kind": e.kind,
                "summary": e.summary,
                "meta": json.dumps(e.meta, sort_keys=True),
                "prev_hash": e.prev_hash,
                "entry_hash": e.entry_hash,
            })
        return rows
