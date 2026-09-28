"""Prime-indexed semantic encoding and deterministic rotations.

This module implements the mathematical foundation for the Rotational Prime Ontology:

1. Prime encoding maps semantic concepts to stable prime indices.
2. Rotational operators apply deterministic state transformations in finite modular space.

Both are purely deterministic — identical inputs always produce identical outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from typing import Iterable


def _is_prime(value: int) -> bool:
    """Check if a value is prime."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _primes() -> Iterable[int]:
    """Generate infinite sequence of prime numbers."""
    candidate = 2
    while True:
        if _is_prime(candidate):
            yield candidate
        candidate += 1


class PrimeEncoder:
    """Map stable, ordered concepts to prime numbers.

    The mapping is local to an encoder instance and can be serialized through
    ``mapping``. Explicit registration keeps encoding deterministic and avoids
    relying on Python's randomized hash function.

    Example:
        >>> encoder = PrimeEncoder(["risk", "safety", "welfare"])
        >>> encoder.mapping
        {'risk': 2, 'safety': 3, 'welfare': 5}
        >>> encoder.prime("risk")
        2
        >>> encoder.encode(["risk", "welfare"])
        {'risk': 2, 'welfare': 5}
    """

    def __init__(self, concepts: Iterable[str] = ()) -> None:
        """Initialize encoder with optional pre-registered concepts."""
        self._mapping: dict[str, int] = {}
        for concept in concepts:
            self.register(concept)

    @property
    def mapping(self) -> dict[str, int]:
        """Return a copy of the concept-to-prime mapping."""
        return dict(self._mapping)

    def register(self, concept: str) -> int:
        """Register a concept and return its assigned prime.

        If already registered, returns the existing prime without modification.
        """
        concept = self._validate_concept(concept)
        if concept not in self._mapping:
            used = set(self._mapping.values())
            self._mapping[concept] = next(p for p in _primes() if p not in used)
        return self._mapping[concept]

    def encode(self, concepts: Iterable[str]) -> dict[str, int]:
        """Batch-register concepts and return their encoding."""
        return {concept: self.register(concept) for concept in concepts}

    def prime(self, concept: str) -> int:
        """Look up the prime assigned to a concept.

        Raises KeyError if the concept has not been registered.
        """
        return self._mapping[self._validate_concept(concept)]

    @staticmethod
    def _validate_concept(concept: str) -> str:
        """Validate and normalize a concept string."""
        if not isinstance(concept, str) or not concept.strip():
            raise ValueError("concept must be a non-empty string")
        return concept.strip()


@dataclass(frozen=True)
class RotationalOperator:
    """Rotate an integer state in a finite, deterministic state space.

    State space is modular arithmetic: all operations wrap within [0, modulus).
    Useful for representing cyclic state transitions, risk levels, protection
    bands, or any bounded decision dimension.

    Example:
        >>> op = RotationalOperator(10)
        >>> op.apply(7, 5)  # (7 + 5) % 10
        2
        >>> op.inverse(2, 5)  # (2 - 5) % 10 = -3 % 10
        7
        >>> op.is_coprime(3)  # gcd(3, 10) == 1
        True
    """

    modulus: int = 360

    def __post_init__(self) -> None:
        """Validate modulus is positive."""
        if self.modulus <= 0:
            raise ValueError("modulus must be positive")

    def apply(self, state: int, amount: int) -> int:
        """Rotate state forward by amount within the modular space."""
        return (state + amount) % self.modulus

    def inverse(self, state: int, amount: int) -> int:
        """Rotate state backward by amount (undoes apply)."""
        return self.apply(state, -amount)

    def compose(self, *amounts: int) -> int:
        """Chain multiple rotations, starting from 0."""
        result = 0
        for amount in amounts:
            result = self.apply(result, amount)
        return result

    def is_coprime(self, amount: int) -> bool:
        """Check if amount and modulus are coprime (gcd = 1).

        Coprime rotations are invertible over the full state space.
        """
        return gcd(amount, self.modulus) == 1
