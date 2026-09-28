"""Paired temporal memory with append-only event history.

This module implements a deterministic, auditable memory system that:
- Stores historical decision states in insertion order (append-only).
- Maintains explicit correlations (edges) between states.
- Ensures all operations are reproducible and traceable.

Memory is immutable once written, enabling governance-grade auditability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    """Current UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class MemoryCorrelation:
    """A directed relationship between two temporal records.

    Represents an edge in the decision history graph, capturing:
    - Source and target record IDs
    - Strength (0.0–1.0) of the relationship
    - Type of relation (causal, contextual, etc.)

    Example:
        >>> corr = MemoryCorrelation("state_1", "state_2", 0.85, "causal")
        >>> corr.strength
        0.85
    """

    source_id: str
    target_id: str
    strength: float
    relation: str = "related"

    def __post_init__(self) -> None:
        """Validate strength is normalized."""
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")


@dataclass(frozen=True)
class MemoryRecord:
    """A timestamped snapshot of a decision state.

    Example:
        >>> record = MemoryRecord("state_1", {"risk": 0.8, "action": "escalate"})
        >>> record.id
        'state_1'
        >>> record.state["risk"]
        0.8
    """

    id: str
    state: dict[str, Any]
    timestamp: datetime = field(default_factory=_now)


class PairedTemporalMemory:
    """Store state pairs and their correlations in insertion order.

    Memory is append-only: once a record is stored, it cannot be modified.
    Correlations are explicit edges that must reference existing records.

    This enables:
    - Complete auditability (all state history)
    - Temporal reasoning (ordered records)
    - Causal tracking (explicit correlations)

    Example:
        >>> memory = PairedTemporalMemory()
        >>> r1 = memory.remember("initial", {"risk": 0.3})
        >>> r2 = memory.remember("escalated", {"risk": 0.8})
        >>> corr = memory.correlate("initial", "escalated", 0.9, "causal")
        >>> len(memory.records)
        2
        >>> len(memory.related_to("initial"))
        1
    """

    def __init__(self) -> None:
        """Initialize empty memory."""
        self._records: dict[str, MemoryRecord] = {}
        self._correlations: list[MemoryCorrelation] = []

    @property
    def records(self) -> tuple[MemoryRecord, ...]:
        """Return all stored records in insertion order."""
        return tuple(self._records.values())

    @property
    def correlations(self) -> tuple[MemoryCorrelation, ...]:
        """Return all correlations in insertion order."""
        return tuple(self._correlations)

    def remember(self, record_id: str, state: dict[str, Any]) -> MemoryRecord:
        """Store a new state record.

        Args:
            record_id: Unique identifier for this record.
            state: Dictionary of state values (will be copied).

        Returns:
            The created MemoryRecord.

        Raises:
            ValueError: If record_id is empty or already exists.
        """
        if not record_id.strip():
            raise ValueError("record_id must not be empty")
        if record_id in self._records:
            raise ValueError(f"record already exists: {record_id}")
        record = MemoryRecord(record_id, dict(state))
        self._records[record_id] = record
        return record

    def correlate(
        self,
        source_id: str,
        target_id: str,
        strength: float,
        relation: str = "related",
    ) -> MemoryCorrelation:
        """Create a correlation between two existing records.

        Args:
            source_id: ID of the source record.
            target_id: ID of the target record.
            strength: Correlation strength (0.0–1.0).
            relation: Type of relationship (default: "related").

        Returns:
            The created MemoryCorrelation.

        Raises:
            KeyError: If either record does not exist.
        """
        if source_id not in self._records or target_id not in self._records:
            raise KeyError("both records must exist before correlating them")
        correlation = MemoryCorrelation(source_id, target_id, strength, relation)
        self._correlations.append(correlation)
        return correlation

    def related_to(self, record_id: str) -> tuple[MemoryCorrelation, ...]:
        """Return all correlations touching a given record.

        Returns edges where record_id is either source or target.
        """
        return tuple(
            c for c in self._correlations
            if c.source_id == record_id or c.target_id == record_id
        )

    def get_record(self, record_id: str) -> MemoryRecord:
        """Retrieve a record by ID.

        Raises KeyError if not found.
        """
        return self._records[record_id]
