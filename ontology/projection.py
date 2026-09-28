"""Deterministic risk analysis and protection projection.

This module transforms raw risk factors into auditable protective recommendations:

1. RiskAnalyzer: Compute normalized risk scores from weighted factors.
2. ProtectionProjector: Map risk levels to domain-neutral actions.

All computations are deterministic and domain-agnostic, supporting
public safety, child welfare, risk management, and AI governance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class RiskResult:
    """Result of risk analysis.

    Attributes:
        score: Normalized risk score (0.0–1.0).
        level: Risk band ("low", "medium", "high").
        factors: Tuple of input factors used in calculation.

    Example:
        >>> result = RiskResult(0.75, "high", ())
        >>> result.level
        'high'
    """

    score: float
    level: str
    factors: tuple[dict[str, Any], ...]


class RiskAnalyzer:
    """Calculate a normalized weighted risk score from factor mappings.

    Each factor is a dictionary with:
    - "value": Numeric contribution (0.0–1.0)
    - "weight": Importance multiplier (default 1.0)
    - Other fields are preserved for audit/explanation

    The weighted mean is computed, then normalized to [0, 1], and mapped to a risk level:
    - 0.00–0.33: "low"
    - 0.34–0.66: "medium"
    - 0.67–1.00: "high"

    Example:
        >>> analyzer = RiskAnalyzer()
        >>> result = analyzer.analyze([
        ...     {"value": 0.8, "weight": 1.0},
        ...     {"value": 0.3, "weight": 0.5}
        ... ])
        >>> result.level
        'medium'
        >>> result.score  # (0.8*1 + 0.3*0.5) / 1.5 = 0.633
        0.633333
    """

    def analyze(self, factors: Iterable[dict[str, Any]]) -> RiskResult:
        """Analyze risk from a collection of factors.

        Args:
            factors: Iterable of factor dictionaries.

        Returns:
            RiskResult with score, level, and normalized factors.
        """
        normalized = tuple(dict(factor) for factor in factors)

        # Empty input returns "low"
        if not normalized:
            return RiskResult(0.0, "low", ())

        # Compute weighted average
        weighted_total = sum(
            float(f.get("value", 0.0)) * float(f.get("weight", 1.0))
            for f in normalized
        )
        weights = sum(float(f.get("weight", 1.0)) for f in normalized)

        # Normalize to [0, 1]
        score = (
            max(0.0, min(1.0, weighted_total / weights))
            if weights
            else 0.0
        )

        # Map to risk level
        level = (
            "high" if score >= 0.67
            else "medium" if score >= 0.34
            else "low"
        )

        return RiskResult(round(score, 6), level, normalized)


class ProtectionProjector:
    """Turn risk results into transparent, domain-neutral recommendations.

    Maps risk levels to protective actions:
    - "low" → "monitor"
    - "medium" → "targeted_intervention"
    - "high" → "immediate_protection"

    The projection includes:
    - Risk score and level
    - Recommended action
    - List of constraints (policies, legal requirements)
    - Explanation of the reasoning

    Example:
        >>> analyzer = RiskAnalyzer()
        >>> result = analyzer.analyze([{"value": 0.8, "weight": 1.0}])
        >>> projector = ProtectionProjector()
        >>> projection = projector.project(result, ["legal_compliance"])
        >>> projection["recommended_action"]
        'immediate_protection'
        >>> projection["constraints"]
        ['legal_compliance']
    """

    def project(
        self,
        result: RiskResult,
        constraints: Iterable[str] = (),
    ) -> dict[str, Any]:
        """Project a risk result into a protection recommendation.

        Args:
            result: Output from RiskAnalyzer.analyze().
            constraints: List of domain constraints to include in recommendation.

        Returns:
            Dictionary with:
            - risk_score: Numeric risk score
            - risk_level: Risk band
            - recommended_action: Domain-neutral action
            - constraints: List of constraints
            - explanation: Human-readable reasoning
        """
        actions = {
            "low": "monitor",
            "medium": "targeted_intervention",
            "high": "immediate_protection",
        }

        return {
            "risk_score": result.score,
            "risk_level": result.level,
            "recommended_action": actions[result.level],
            "constraints": list(constraints),
            "explanation": f"Action selected from deterministic risk band: {result.level}.",
        }

    @staticmethod
    def action_for_level(level: str) -> str:
        """Return the protective action for a given risk level.

        Useful for quick lookups without creating a full projection.
        """
        actions = {
            "low": "monitor",
            "medium": "targeted_intervention",
            "high": "immediate_protection",
        }
        return actions.get(level, "unknown")
