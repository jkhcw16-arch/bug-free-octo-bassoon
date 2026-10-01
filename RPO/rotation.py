def normalize_raw(category: str, value: float) -> float:
    # Simple placeholder normalization → [0,1]
    return max(0.0, min(value / 100.0, 1.0))

def R1_normalize(raw: dict[str, float]) -> dict[str, float]:
    return {cat: normalize_raw(cat, val) for cat, val in raw.items()}

def R2_align(agency: dict[str, float], subject: dict[str, float]) -> dict[str, float]:
    return {cat: (agency[cat] + subject[cat]) / 2.0 for cat in agency}

def response_strength(category: str, gamma: float) -> float:
    return max(0.0, min(gamma, 2.0))

def R3_response(aligned: dict[str, float]) -> dict[str, float]:
    return {cat: response_strength(cat, val) for cat, val in aligned.items()}
