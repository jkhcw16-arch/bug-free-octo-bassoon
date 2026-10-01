from rpo.memory import PairedMemory

def test_memory_symmetry():
    mem = PairedMemory()
    sigma = 10.0
    projected = {"HeatRisk": 5.0, "Humidity": 3.0}
    mem.update(sigma, projected)
    assert mem.M_a == mem.M_s

def test_memory_accumulation():
    mem = PairedMemory()
    sigma = 10.0
    projected = {"HeatRisk": 5.0}
    mem.update(sigma, projected)
    first = mem.M_a["HeatRisk"]
    mem.update(sigma, projected)
    second = mem.M_a["HeatRisk"]
    assert second > first
