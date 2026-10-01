from math import prod
from .prime_table import get_prime

def encode_state(indicators: dict[str, float]) -> float:
    return prod(get_prime(cat) ** alpha for cat, alpha in indicators.items())
