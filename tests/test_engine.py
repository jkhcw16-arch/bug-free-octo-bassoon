from rpo.engine import run_rpo
from rpo.memory import PairedMemory

def test_engine_basic():
    raw = {"HeatRisk": 95, "Humidity": 80}
    agency = {"HeatRisk": 0.9, "Humidity": 0.7}
    subject = {"HeatRisk": 0.8, "Humidity": 0.6}
    memory = PairedMemory()
    intensities = run_rpo(raw, agency, subject, rho=2.0, memory=memory)
    assert all(0.0 <= v <= 1.0 for v in intensities.values())
