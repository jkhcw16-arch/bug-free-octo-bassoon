from .prime_table import get_prime

def project_role(exponents: dict[str, float], rho: float) -> dict[str, float]:
    return {cat: get_prime(cat) ** (exp * rho) for cat, exp in exponents.items()}
