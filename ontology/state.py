"""Decision state, transitions, and constraint validation.

This module provides the state representation and validation layer for decisions:

1. DecisionState: Immutable snapshots of decision context.
2. StateTransition: Proposed changes from one state to another.
3. ConstraintChecker: Validates transitions against domain rules.

All types are designed for deterministic, auditable decision-making.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass(frozen=True)
class DecisionState:
    """Immutable state snapshot used by the decision pipeline.

    Represents a point-in-time view of decision context, including:
    - domain: The application area (e.g., "public_safety", "child_welfare")
    - state_id: Unique identifier for this state
    - values: Arbitrary key-value context data
    - timestamp: When this state was created

    Example:
        >>> state = DecisionState("s1", "public_safety", {"threat": 0.8})
        >>> state.domain
        'public_safety'
        >>> new_state = state.with_values(action="escalate")
        >>> new_state.values
        {'threat': 0.8, 'action': 'escalate'}
    """

    state_id: str
    domain: str
    values: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def with_values(self, **updates: Any) -> DecisionState:
        """Create a new state with updated values.

        Timestamp remains the same; supply a new timestamp separately if needed.
        """
        values = {**self.values, **updates}
        return DecisionState(self.state_id, self.domain, values, self.timestamp)

    def __str__(self) -> str:
        return f"DecisionState(id={self.state_id}, domain={self.domain}, keys={list(self.values.keys())})"


@dataclass(frozen=True)
class StateTransition:
    """A proposed change from one decision state to another.

    Captures the "before" and "after" along with reasoning, enabling
    full auditability and constraint checking.

    Example:
        >>> s1 = DecisionState("s1", "test", {"approved": False})
        >>> s2 = s1.with_values(approved=True)
        >>> transition = StateTransition(s1, s2, "manual_review")
        >>> transition.reason
        'manual_review'
    """

    source: DecisionState
    target: DecisionState
    reason: str

    def __str__(self) -> str:
        return f"StateTransition({self.source.state_id} -> {self.target.state_id}, reason={self.reason})"


class ConstraintChecker:
    """Run named predicates against a state transition.

    Constraints are domain rules that must hold for a transition to be valid.
    Each constraint is a named boolean predicate that examines the transition.

    Example:
        >>> def has_approval(t):
        ...     return t.target.values.get("approved", False)
        >>> checker = ConstraintChecker({"approval": has_approval})
        >>> s1 = DecisionState("s1", "test", {"approved": False})
        >>> s2 = s1.with_values(approved=True)
        >>> t = StateTransition(s1, s2, "review")
        >>> checker.is_valid(t)
        True
        >>> checker.validate(t)
        {'approval': True}
    """

    def __init__(
        self,
        constraints: dict[str, Callable[[StateTransition], bool]] | None = None,
    ) -> None:
        """Initialize with optional constraint predicates."""
        self.constraints = constraints or {}

    def add(
        self,
        name: str,
        predicate: Callable[[StateTransition], bool],
    ) -> None:
        """Add a named constraint predicate.

        Args:
            name: Human-readable constraint name.
            predicate: Function taking a StateTransition and returning bool.

        Raises:
            ValueError: If name is empty.
        """
        if not name.strip():
            raise ValueError("constraint name must not be empty")
        self.constraints[name] = predicate

    def validate(self, transition: StateTransition) -> dict[str, bool]:
        """Run all constraints and return results by name.

        Returns a dictionary mapping constraint names to pass/fail.
        All constraints are evaluated; a single failure doesn't stop others.
        """
        return {
            name: bool(predicate(transition))
            for name, predicate in self.constraints.items()
        }

    def is_valid(self, transition: StateTransition) -> bool:
        """Check if all constraints pass for a transition.

        Returns True only if ALL constraints return True.
        """
        return all(self.validate(transition).values())

    def failed_constraints(self, transition: StateTransition) -> dict[str, bool]:
        """Return only the constraints that failed.

        Useful for diagnostic messaging.
        """
        return {name: passed for name, passed in self.validate(transition).items() if not passed}
