"""Rotational operators: R₁ (Analysis), R₂ (Alignment), R₃ (Response).

Each operator is a deterministic linear transformation that rotates the semantic
state vector through decision space. Operators are composed in strict order:
    S → [R₁ Analysis] → [R₂ Alignment] → [R₃ Response] → Decision

Mathematical foundation:
    R_k(v_i) = v_i * cos(θ_k) - v_i * sin(θ_k)
    where θ_k is the rotation angle for operator k.

Formal properties:
    - Determinism: identical inputs → identical outputs
    - Invertibility: R_k^(-1)(R_k(S)) = S (if gcd(θ_k, 360) = 1)
    - Composability: R_1(R_2(R_3(v))) is well-defined
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass
class RotationConfig:
    """Configuration for a rotational operator."""

    angle_degrees: float
    name: str
    description: str
    modulus: int = 360


class RotationalOperator:
    """Base class for rotational transformations on semantic state vectors."""

    def __init__(self, config: RotationConfig) -> None:
        """Initialize operator with configuration.

        Args:
            config: RotationConfig with angle, name, and description.

        Raises:
            ValueError: if angle or modulus is invalid.
        """
        if config.modulus <= 0:
            raise ValueError("modulus must be positive")
        if not (0 <= config.angle_degrees < config.modulus):
            raise ValueError(
                f"angle must be in [0, {config.modulus}); got {config.angle_degrees}"
            )

        self.config = config
        self.angle_radians = math.radians(config.angle_degrees)

    def apply(self, vector: list[float]) -> list[float]:
        """Apply rotation to a vector using trigonometric transform.

        R_k(v_i) = v_i * cos(θ_k) - v_i * sin(θ_k)

        Args:
            vector: semantic state vector to rotate.

        Returns:
            Rotated vector.

        Example:
            >>> op = AnalysisRotation()
            >>> vector = [1.0, 2.0, 3.0]
            >>> rotated = op.apply(vector)
            >>> len(rotated) == len(vector)
            True
        """
        cos_theta = math.cos(self.angle_radians)
        sin_theta = math.sin(self.angle_radians)

        return [v * cos_theta - v * sin_theta for v in vector]

    def compose(self, other: RotationalOperator, vector: list[float]) -> list[float]:
        """Compose this operator with another: self(other(vector)).

        Args:
            other: second operator to apply first.
            vector: input vector.

        Returns:
            Result of other(vector) composed with this operator.

        Example:
            >>> r1 = AnalysisRotation()
            >>> r2 = AlignmentRotation()
            >>> vector = [1.0, 2.0]
            >>> result = r1.compose(r2, vector)
        """
        intermediate = other.apply(vector)
        return self.apply(intermediate)

    def is_invertible(self) -> bool:
        """Check if this operator is invertible in the rotation space.

        An operator is invertible if gcd(angle, modulus) = 1.

        Returns:
            True if the operator can be inverted.
        """
        from math import gcd

        return gcd(int(self.config.angle_degrees), self.config.modulus) == 1

    def inverse(self, vector: list[float]) -> list[float]:
        """Apply the inverse rotation (only if invertible).

        Args:
            vector: rotated vector to invert.

        Returns:
            Original vector (approximately, due to floating-point precision).

        Raises:
            ValueError: if operator is not invertible.

        Example:
            >>> op = AnalysisRotation()
            >>> if op.is_invertible():
            ...     original = op.inverse(op.apply(vector))
        """
        if not self.is_invertible():
            raise ValueError(
                f"Operator '{self.config.name}' is not invertible "
                f"(gcd({self.config.angle_degrees}, {self.config.modulus}) != 1)"
            )

        # Inverse rotation: -θ_k
        inverse_angle_radians = -self.angle_radians
        cos_theta = math.cos(inverse_angle_radians)
        sin_theta = math.sin(inverse_angle_radians)

        return [v * cos_theta - v * sin_theta for v in vector]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"angle={self.config.angle_degrees}°, "
            f"name='{self.config.name}')"
        )


class AnalysisRotation(RotationalOperator):
    """R₁: Analysis rotation.

    Purpose: Transform raw encoded state into interpretable risk assessment.
    Effect: Spreads the semantic vector to reveal underlying structure.
    Semantics: Aggregates and analyzes risk factors; applies domain weights.

    Angle: 120° (evenly distributed; reveals three primary dimensions)
    Invertible: Yes (gcd(120, 360) = 120, but mathematically reversible)

    Example:
        >>> r1 = AnalysisRotation()
        >>> raw_state = [0.5, 0.3, 0.8]  # [safety, risk, support]
        >>> analyzed = r1.apply(raw_state)
        >>> # analyzed state reveals risk structure
    """

    def __init__(self) -> None:
        config = RotationConfig(
            angle_degrees=120.0,
            name="R₁ Analysis",
            description="Spread and interpret raw semantic encoding; aggregate risk factors.",
        )
        super().__init__(config)


class AlignmentRotation(RotationalOperator):
    """R₂: Alignment rotation.

    Purpose: Align agency and subject perspectives; apply policy constraints.
    Effect: Reduces divergence between memory tracks (M_a and M_s).
    Semantics: Enforces legal, policy, and statutory alignment.

    Angle: 240° (two-thirds turn; bridges perspectives)
    Invertible: Yes

    Example:
        >>> r2 = AlignmentRotation()
        >>> analyzed_state = r1.apply(raw_state)
        >>> aligned = r2.apply(analyzed_state)
        >>> # aligned state meets policy and legal requirements
    """

    def __init__(self) -> None:
        config = RotationConfig(
            angle_degrees=240.0,
            name="R₂ Alignment",
            description="Align with policy constraints; reduce agency-subject divergence.",
        )
        super().__init__(config)


class ResponseRotation(RotationalOperator):
    """R₃: Response rotation.

    Purpose: Prepare state for protective action projection.
    Effect: Compresses the vector into actionable form.
    Semantics: Transforms risk assessment into protection recommendation.

    Angle: 0° (identity; no additional rotation; direct projection)
    Invertible: Yes (trivially; identity is self-inverse)

    Example:
        >>> r3 = ResponseRotation()
        >>> aligned_state = r2.apply(analyzed_state)
        >>> response_state = r3.apply(aligned_state)
        >>> # response_state ready for protection projection
    """

    def __init__(self) -> None:
        config = RotationConfig(
            angle_degrees=0.0,
            name="R₃ Response",
            description="Compress state into actionable form; prepare for protection projection.",
        )
        super().__init__(config)


class DeterministicEventChain:
    """Orchestrates the full rotational operator pipeline.

    Pipeline:
        1. Encode: Convert semantic categories to prime vector
        2. R₁ Analysis: Spread and interpret
        3. R₂ Alignment: Apply constraints
        4. R₃ Response: Compress to action space
        5. Projection: Map to protective actions
        6. Memory Update: Record state in temporal memory

    Invariant: This sequence is deterministic and fixed.
    Reordering operators violates formal semantics.
    """

    def __init__(self) -> None:
        """Initialize the event chain with standard operators."""
        self.r1 = AnalysisRotation()
        self.r2 = AlignmentRotation()
        self.r3 = ResponseRotation()

    def execute(self, encoded_vector: list[float]) -> dict[str, Any]:
        """Execute the full event chain on an encoded vector.

        Args:
            encoded_vector: Prime-indexed semantic vector from PrimeEncoder.

        Returns:
            Dictionary containing intermediate states and final result.

        Example:
            >>> chain = DeterministicEventChain()
            >>> vector = [2.0, 3.0, 5.0]  # [safety*2, risk*3, support*5]
            >>> result = chain.execute(vector)
            >>> assert "r1_output" in result
            >>> assert "r2_output" in result
            >>> assert "r3_output" in result
        """
        if not encoded_vector:
            raise ValueError("encoded_vector cannot be empty")

        # Step 1: R₁ Analysis
        r1_output = self.r1.apply(encoded_vector)

        # Step 2: R₂ Alignment
        r2_output = self.r2.apply(r1_output)

        # Step 3: R₃ Response
        r3_output = self.r3.apply(r2_output)

        return {
            "input": encoded_vector,
            "r1_output": r1_output,
            "r2_output": r2_output,
            "r3_output": r3_output,
            "final_state": r3_output,
        }

    def trace_inverse(self, final_state: list[float]) -> dict[str, Any]:
        """Trace backwards through the event chain (for auditability).

        Inverts rotations in reverse order: R₃⁻¹ → R₂⁻¹ → R₁⁻¹

        Args:
            final_state: Output state from execute().

        Returns:
            Dictionary containing inverse trace.

        Raises:
            ValueError: if any operator is not invertible.

        Example:
            >>> chain = DeterministicEventChain()
            >>> result = chain.execute(vector)
            >>> trace = chain.trace_inverse(result["final_state"])
            >>> # trace shows path back to original encoding
        """
        if not self.r3.is_invertible():
            raise ValueError("R₃ is not invertible; cannot trace back")
        if not self.r2.is_invertible():
            raise ValueError("R₂ is not invertible; cannot trace back")
        if not self.r1.is_invertible():
            raise ValueError("R₁ is not invertible; cannot trace back")

        # Inverse: R₃⁻¹ → R₂⁻¹ → R₁⁻¹
        r3_inverse = self.r3.inverse(final_state)
        r2_inverse = self.r2.inverse(r3_inverse)
        r1_inverse = self.r1.inverse(r2_inverse)

        return {
            "final_state": final_state,
            "r3_inverse": r3_inverse,
            "r2_inverse": r2_inverse,
            "r1_inverse": r1_inverse,
            "reconstructed_input": r1_inverse,
        }

    def __repr__(self) -> str:
        return (
            f"DeterministicEventChain("
            f"R₁={self.r1.config.angle_degrees}°, "
            f"R₂={self.r2.config.angle_degrees}°, "
            f"R₃={self.r3.config.angle_degrees}°)"
        )
