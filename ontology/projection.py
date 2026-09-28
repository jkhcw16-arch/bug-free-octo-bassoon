"""Deterministic risk analysis and protection projection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class RiskResult:
    score: float
    level: str
    factors: tuple[dict[str, Any], ...]


class RiskAnalyzer:
    """Calculate a normalized weighted risk score from factor mappings."""

    def analyze(self, factors: Iterable[dict[str, Any]]) -> RiskResult:
        normalized = tuple(dict(factor) for factor in factors)
        if not normalized:
            return RiskResult(0.0, "low", ())
        weighted_total = sum(float(f.get("value", 0.0)) * float(f.get("weight", 1.0)) for f in normalized)
        weights = sum(float(f.get("weight", 1.0)) for f in normalized)
        score = max(0.0, min(1.0, weighted_total / weights)) if weights else 0.0
        level = "high" if score >= 0.67 else "medium" if score >= 0.34 else "low"
        return RiskResult(round(score, 6), level, normalized)


class ProtectionProjector:
    """Turn risk results into transparent, domain-neutral recommendations."""

    def project(self, result: RiskResult, constraints: Iterable[str] = ()) -> dict[str, Any]:
        actions = {"low": "monitor", "medium": "targeted_intervention", "high": "immediate_protection"}
        return {
            "risk_score": result.score,
            "risk_level": result.level,
            "recommended_action": actions[result.level],
            "constraints": list(constraints),
            "explanation": f"Action selected from deterministic risk band: {result.level}.",
        }
