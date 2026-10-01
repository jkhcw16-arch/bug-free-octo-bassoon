# audit.py

def test_deterministic_trace(engine, raw, agency, subject, rho, memory):
    out1 = engine(raw, agency, subject, rho, memory)
    out2 = engine(raw, agency, subject, rho, memory)
    return out1 == out2
