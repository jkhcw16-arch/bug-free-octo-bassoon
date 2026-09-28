"""Paired temporal memory with append-only event history."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class MemoryCorrelation:
    """A directed relationship between two temporal records."""

    source_id: str
    target_id: str
    strength: float
    relation: str = "related"

    def __post_init__(self) -> None:
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")


@dataclass(frozen=True)
class MemoryRecord:
    id: str
    state: dict[str, Any]
    timestamp: datetime = field(default_factory=_now)


class PairedTemporalMemory:
    """Store state pairs and their correlations in insertion order."""

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}
        self._correlations: list[MemoryCorrelation] = []

    @property
    def records(self) -> tuple[MemoryRecord, ...]:
        return tuple(self._records.values())

    @property
    def correlations(self) -> tuple[MemoryCorrelation, ...]:
        return tuple(self._correlations)

    def remember(self, record_id: str, state: dict[str, Any]) -> MemoryRecord:
        if not record_id.strip():
            raise ValueError("record_id must not be empty")
        if record_id in self._records:
            raise ValueError(f"record already exists: {record_id}")
        record = MemoryRecord(record_id, dict(state))
        self._records[record_id] = record
        return record

    def correlate(self, source_id: str, target_id: str, strength: float, relation: str = "related") -> MemoryCorrelation:
        if source_id not in self._records or target_id not in self._records:
            raise KeyError("both records must exist before correlating them")
        correlation = MemoryCorrelation(source_id, target_id, strength, relation)
        self._correlations.append(correlation)
        return correlation

    def related_to(self, record_id: str) -> tuple[MemoryCorrelation, ...]:
        return tuple(c for c in self._correlations if c.source_id == record_id or c.target_id == record_id)
