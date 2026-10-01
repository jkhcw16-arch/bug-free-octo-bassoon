# memory.py

def test_memory_symmetry(memory, sigma, projected):
    before_a = memory.M_a.copy()
    before_s = memory.M_s.copy()
    memory.update(sigma, projected)
    return memory.M_a == memory.M_s
