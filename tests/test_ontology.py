"""Unit tests for the Rotational Prime Ontology.

Tests validate:
- Determinism: identical inputs produce identical outputs
- Immutability: state objects cannot be modified
- Constraint satisfaction: validators work correctly
- Auditability: memory preserves complete history
"""

import pytest

from ontology.core import PrimeEncoder, RotationalOperator
from ontology.memory import MemoryCorrelation, MemoryRecord, PairedTemporalMemory
from ontology.projection import ProtectionProjector, RiskAnalyzer, RiskResult
from ontology.state import ConstraintChecker, DecisionState, StateTransition


class TestPrimeEncoder:
    """Tests for PrimeEncoder."""

    def test_prime_encoding_is_stable_and_unique(self) -> None:
        """Concepts map to the same primes across multiple registrations."""
        encoder = PrimeEncoder(["risk", "protection"])
        assert encoder.mapping == {"risk": 2, "protection": 3}
        assert encoder.register("risk") == 2
        assert encoder.register("protection") == 3

    def test_concepts_are_assigned_in_order(self) -> None:
        """Concepts are assigned to primes 2, 3, 5, 7, ... in registration order."""
        encoder = PrimeEncoder()
        assert encoder.register("alpha") == 2
        assert encoder.register("beta") == 3
        assert encoder.register("gamma") == 5

    def test_encode_batch_registers_multiple_concepts(self) -> None:
        """encode() batch-registers and returns a mapping."""
        encoder = PrimeEncoder()
        result = encoder.encode(["risk", "safety", "welfare"])
        assert result == {"risk": 2, "safety": 3, "welfare": 5}

    def test_invalid_concepts_raise_error(self) -> None:
        """Empty or non-string concepts raise ValueError."""
        encoder = PrimeEncoder()
        with pytest.raises(ValueError):
            encoder.register("")
        with pytest.raises(ValueError):
            encoder.register("   ")


class TestRotationalOperator:
    """Tests for RotationalOperator."""

    def test_rotation_wraps_and_inverts(self) -> None:
        """apply() and inverse() are inverses in modular arithmetic."""
        operator = RotationalOperator(10)
        assert operator.apply(8, 5) == 3
        assert operator.inverse(3, 5) == 8

    def test_compose_chains_rotations(self) -> None:
        """compose() chains multiple rotation amounts."""
        operator = RotationalOperator(360)
        result = operator.compose(90, 180, 45)
        assert result == 315

    def test_coprime_check(self) -> None:
        """is_coprime() identifies coprime amounts."""
        operator = RotationalOperator(10)
        assert operator.is_coprime(3) is True
        assert operator.is_coprime(5) is False
        assert operator.is_coprime(7) is True

    def test_invalid_modulus_raises_error(self) -> None:
        """Modulus must be positive."""
        with pytest.raises(ValueError):
            RotationalOperator(0)
        with pytest.raises(ValueError):
            RotationalOperator(-10)


class TestPairedTemporalMemory:
    """Tests for PairedTemporalMemory."""

    def test_memory_requires_existing_records_for_correlation(self) -> None:
        """correlate() raises KeyError if records don't exist."""
        memory = PairedTemporalMemory()
        memory.remember("a", {"value": 1})
        with pytest.raises(KeyError):
            memory.correlate("a", "missing", 0.5)

    def test_memory_stores_and_retrieves_records(self) -> None:
        """remember() stores records; get_record() retrieves them."""
        memory = PairedTemporalMemory()
        r1 = memory.remember("r1", {"state": "initial"})
        assert r1.id == "r1"
        assert r1.state == {"state": "initial"}
        retrieved = memory.get_record("r1")
        assert retrieved is r1

    def test_memory_prevents_duplicate_records(self) -> None:
        """remember() raises ValueError on duplicate ID."""
        memory = PairedTemporalMemory()
        memory.remember("r1", {"value": 1})
        with pytest.raises(ValueError):
            memory.remember("r1", {"value": 2})

    def test_memory_tracks_correlations(self) -> None:
        """correlate() creates edges; related_to() retrieves them."""
        memory = PairedTemporalMemory()
        r1 = memory.remember("r1", {})
        r2 = memory.remember("r2", {})
        corr = memory.correlate("r1", "r2", 0.8, "causal")
        assert corr.strength == 0.8
        assert corr.relation == "causal"
        related = memory.related_to("r1")
        assert len(related) == 1
        assert related[0] is corr

    def test_correlation_strength_must_be_normalized(self) -> None:
        """MemoryCorrelation rejects strength outside [0, 1]."""
        with pytest.raises(ValueError):
            MemoryCorrelation("a", "b", 1.5)
        with pytest.raises(ValueError):
            MemoryCorrelation("a", "b", -0.1)


class TestDecisionState:
    """Tests for DecisionState."""

    def test_state_is_immutable(self) -> None:
        """DecisionState is frozen; mutations raise error."""
        state = DecisionState("s1", "test")
        with pytest.raises(AttributeError):
            state.values["key"] = "value"  # type: ignore

    def test_with_values_creates_new_state(self) -> None:
        """with_values() returns new state; original unchanged."""
        s1 = DecisionState("s1", "test", {"a": 1})
        s2 = s1.with_values(b=2)
        assert s1.values == {"a": 1}
        assert s2.values == {"a": 1, "b": 2}
        assert s1 is not s2


class TestStateTransition:
    """Tests for StateTransition."""

    def test_transition_captures_before_and_after(self) -> None:
        """StateTransition holds source, target, and reason."""
        s1 = DecisionState("s1", "test", {"approved": False})
        s2 = s1.with_values(approved=True)
        transition = StateTransition(s1, s2, "manual_review")
        assert transition.source is s1
        assert transition.target is s2
        assert transition.reason == "manual_review"


class TestConstraintChecker:
    """Tests for ConstraintChecker."""

    def test_constraint_checker_validates_transitions(self) -> None:
        """Checker runs predicates and reports pass/fail."""
        source = DecisionState("a", "test")
        target = source.with_values(approved=True)
        transition = StateTransition(source, target, "review")
        checker = ConstraintChecker(
            {"approved": lambda t: t.target.values["approved"]}
        )
        assert checker.is_valid(transition) is True
        assert checker.validate(transition) == {"approved": True}

    def test_multiple_constraints_all_must_pass(self) -> None:
        """is_valid() returns True only if all constraints pass."""
        s1 = DecisionState("s1", "test", {"approved": False})
        s2 = s1.with_values(approved=True, reviewed=False)
        t = StateTransition(s1, s2, "review")
        checker = ConstraintChecker()
        checker.add("approved", lambda x: x.target.values["approved"])
        checker.add("reviewed", lambda x: x.target.values["reviewed"])
        assert checker.is_valid(t) is False
        assert "reviewed" in checker.failed_constraints(t)


class TestRiskAnalyzer:
    """Tests for RiskAnalyzer."""

    def test_risk_projection(self) -> None:
        """Risk from single factor is mapped to level correctly."""
        result = RiskAnalyzer().analyze([{"value": 0.8, "weight": 1}])
        assert result.level == "high"
        assert result.score == 0.8

    def test_weighted_risk_calculation(self) -> None:
        """Weighted average of factors is computed correctly."""
        result = RiskAnalyzer().analyze(
            [{"value": 0.8, "weight": 1.0}, {"value": 0.3, "weight": 0.5}]
        )
        expected_score = (0.8 * 1.0 + 0.3 * 0.5) / 1.5
        assert result.score == round(expected_score, 6)

    def test_empty_factors_return_low_risk(self) -> None:
        """No factors defaults to low risk."""
        result = RiskAnalyzer().analyze([])
        assert result.level == "low"
        assert result.score == 0.0

    def test_risk_levels_are_correct(self) -> None:
        """Risk bands are [0, 0.34), [0.34, 0.67), [0.67, 1.0]."""
        analyzer = RiskAnalyzer()
        assert analyzer.analyze([{"value": 0.1}]).level == "low"
        assert analyzer.analyze([{"value": 0.5}]).level == "medium"
        assert analyzer.analyze([{"value": 0.8}]).level == "high"


class TestProtectionProjector:
    """Tests for ProtectionProjector."""

    def test_protection_projection_maps_levels_to_actions(self) -> None:
        """Risk levels map to protective actions."""
        projector = ProtectionProjector()
        low_result = RiskResult(0.1, "low", ())
        med_result = RiskResult(0.5, "medium", ())
        high_result = RiskResult(0.8, "high", ())
        assert projector.project(low_result)["recommended_action"] == "monitor"
        assert (
            projector.project(med_result)["recommended_action"]
            == "targeted_intervention"
        )
        assert (
            projector.project(high_result)["recommended_action"]
            == "immediate_protection"
        )

    def test_projection_includes_constraints(self) -> None:
        """Constraints are included in projection."""
        projector = ProtectionProjector()
        result = RiskResult(0.5, "medium", ())
        projection = projector.project(result, ["legal_compliance", "policy_x"])
        assert projection["constraints"] == ["legal_compliance", "policy_x"]

    def test_action_for_level_helper(self) -> None:
        """action_for_level() provides quick action lookup."""
        assert ProtectionProjector.action_for_level("low") == "monitor"
        assert ProtectionProjector.action_for_level("medium") == "targeted_intervention"
        assert ProtectionProjector.action_for_level("high") == "immediate_protection"
