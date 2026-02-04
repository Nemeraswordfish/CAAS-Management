from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List

from caas_management.models import AuditEntry


@dataclass
class AuditTrail:
    entries: List[AuditEntry]

    def __init__(self) -> None:
        self.entries = []

    def append(self, entry: AuditEntry) -> AuditEntry:
        previous_hash = self.entries[-1].hash if self.entries else None
        entry.previous_hash = previous_hash
        entry.hash = self._hash_entry(entry)
        self.entries.append(entry)
        return entry

    def _hash_entry(self, entry: AuditEntry) -> str:
        payload = f"{entry.action}|{entry.metadata}|{entry.timestamp.isoformat()}|{entry.previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
