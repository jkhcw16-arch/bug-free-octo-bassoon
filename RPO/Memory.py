def memory_update(memory: dict[str, float],
                  sigma: float,
                  projected: dict[str, float]) -> dict[str, float]:
    delta = sum(projected.values()) * 0.001
    return {k: memory.get(k, 0.0) + delta for k in projected}

class PairedMemory:
    def __init__(self) -> None:
        self.M_a: dict[str, float] = {}
        self.M_s: dict[str, float] = {}

    def update(self, sigma: float, projected: dict[str, float]) -> None:
        self.M_a = memory_update(self.M_a, sigma, projected)
        self.M_s = memory_update(self.M_s, sigma, projected)
