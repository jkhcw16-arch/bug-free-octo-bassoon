def intensity_mapping(category: str, projected_value: float) -> float:
    # Placeholder bounded mapping → [0,1]
    return projected_value / (projected_value + 10.0)

def map_intensities(projected: dict[str, float]) -> dict[str, float]:
    return {cat: max(0.0, min(intensity_mapping(cat, val), 1.0))
            for cat, val in projected.items()}
