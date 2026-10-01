def select_least_intrusive(actions: list[dict], P_min: float) -> dict:
    feasible = [a for a in actions if a["protection"] >= P_min]
    if not feasible:
        raise ValueError("No adequate actions available")
    return min(feasible, key=lambda a: a["intrusion"])
