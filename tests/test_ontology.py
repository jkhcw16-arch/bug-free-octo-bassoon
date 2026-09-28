import pytest

from ontology.core import PrimeEncoder, RotationalOperator
from ontology.memory import PairedTemporalMemory
from ontology.projection import ProtectionProjector, RiskAnalyzer
from ontology.state import ConstraintChecker, DecisionState, StateTransition


def test_prime_encoding_is_stable_and_unique():
    encoder = PrimeEncoder(["risk", "protection"])
    assert encoder.mapping == {"risk": 2, "protection": 3}
    assert encoder.register("risk") == 2


def test_rotation_wraps_and_inverts():
    operator = RotationalOperator(10)
    assert operator.apply(8, 5) == 3
    assert operator.inverse(3, 5) == 8


def test_memory_requires_existing_records_for_correlation():
    memory = PairedTemporalMemory()
    memory.remember("a", {"value": 1})
    with pytest.raises(KeyError):
        memory.correlate("a", "missing", 0.5)


def test_constraint_checker():
    source = DecisionState("a", "test")
    target = source.with_values(approved=True)
    transition = StateTransition(source, target, "review")
    checker = ConstraintChecker({"approved": lambda item: item.target.values["approved"]})
    assert checker.is_valid(transition)


def test_risk_projection():
    result = RiskAnalyzer().analyze([{"value": 0.8, "weight": 1}])
    projection = ProtectionProjector().project(result)
    assert result.level == "high"
    assert projection["recommended_action"] == "immediate_protection"
