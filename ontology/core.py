"""Prime-indexed semantic encoding and deterministic rotations."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from typing import Iterable


def _is_prime(value: int) -> bool:
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
    """

    def __init__(self, concepts: Iterable[str] = ()) -> None:
        self._mapping: dict[str, int] = {}
        for concept in concepts:
            self.register(concept)

    @property
    def mapping(self) -> dict[str, int]:
        return dict(self._mapping)

    def register(self, concept: str) -> int:
        concept = self._validate_concept(concept)
        if concept not in self._mapping:
            used = set(self._mapping.values())
            self._mapping[concept] = next(p for p in _primes() if p not in used)
        return self._mapping[concept]

    def encode(self, concepts: Iterable[str]) -> dict[str, int]:
        return {concept: self.register(concept) for concept in concepts}

    def prime(self, concept: str) -> int:
        return self._mapping[self._validate_concept(concept)]

    @staticmethod
    def _validate_concept(concept: str) -> str:
        if not isinstance(concept, str) or not concept.strip():
            raise ValueError("concept must be a non-empty string")
        return concept.strip()


@dataclass(frozen=True)
class RotationalOperator:
    """Rotate an integer state in a finite, deterministic state space."""

    modulus: int = 360

    def __post_init__(self) -> None:
        if self.modulus <= 0:
            raise ValueError("modulus must be positive")

    def apply(self, state: int, amount: int) -> int:
        return (state + amount) % self.modulus

    def inverse(self, state: int, amount: int) -> int:
        return self.apply(state, -amount)

    def compose(self, *amounts: int) -> int:
        result = 0
        for amount in amounts:
            result = self.apply(result, amount)
        return result

    def is_coprime(self, amount: int) -> bool:
        return gcd(amount, self.modulus) == 1
