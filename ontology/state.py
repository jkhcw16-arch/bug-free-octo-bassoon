"""Decision state, transitions, and constraint validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass(frozen=True)
class DecisionState:
    """Immutable state snapshot used by the decision pipeline."""

    state_id: str
    domain: str
    values: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def with_values(self, **updates: Any) -> "DecisionState":
        values = {**self.values, **updates}
        return DecisionState(self.state_id, self.domain, values, self.timestamp)


@dataclass(frozen=True)
class StateTransition:
    """A proposed change from one decision state to another."""

    source: DecisionState
    target: DecisionState
    reason: str


class ConstraintChecker:
    """Run named predicates against a state transition."""

    def __init__(self, constraints: dict[str, Callable[[StateTransition], bool]] | None = None) -> None:
        self.constraints = constraints or {}

    def add(self, name: str, predicate: Callable[[StateTransition], bool]) -> None:
        if not name.strip():
            raise ValueError("constraint name must not be empty")
        self.constraints[name] = predicate

    def validate(self, transition: StateTransition) -> dict[str, bool]:
        return {name: bool(predicate(transition)) for name, predicate in self.constraints.items()}

    def is_valid(self, transition: StateTransition) -> bool:
        return all(self.validate(transition).values())
