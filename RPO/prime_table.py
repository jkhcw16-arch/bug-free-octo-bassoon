PRIMES = {
    "HeatRisk": 2,
    "Humidity": 3,
    "WindSpeed": 5,
    "AirQuality": 7,
    "PopulationVulnerability": 11,
    # TODO: extend with full Annex A
}

def get_prime(category: str) -> int:
    try:
        return PRIMES[category]
    except KeyError:
        raise ValueError(f"Unknown category: {category}")
