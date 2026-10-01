import pytest
from rpo.prime_table import PRIMES, get_prime
from rpo.encoding import encode_state

def test_prime_uniqueness():
    primes = list(PRIMES.values())
    assert len(primes) == len(set(primes))

def test_prime_lookup():
    assert get_prime("HeatRisk") == 2
    with pytest.raises(ValueError):
        get_prime("UnknownCategory")

def test_collision_free_encoding():
    indicators = {"HeatRisk": 0.4, "Humidity": 0.7, "WindSpeed": 0.2}
    sigma = encode_state(indicators)
    # Encode twice → identical
    sigma2 = encode_state(indicators)
    assert sigma == sigma2
