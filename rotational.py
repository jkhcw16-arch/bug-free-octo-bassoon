# rotational.py

def test_R1_determinism(raw):
    return R1_normalize(raw) == R1_normalize(raw)
