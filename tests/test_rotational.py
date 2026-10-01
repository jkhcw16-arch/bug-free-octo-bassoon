from rpo.rotation import R1_normalize, R2_align, R3_response

def test_R1_normalization():
    raw = {"HeatRisk": 95, "Humidity": 80}
    norm = R1_normalize(raw)
    assert norm["HeatRisk"] == 0.95
    assert norm["Humidity"] == 0.80

def test_R2_alignment():
    agency = {"HeatRisk": 0.9, "Humidity": 0.7}
    subject = {"HeatRisk": 0.8, "Humidity": 0.6}
    aligned = R2_align(agency, subject)
    assert aligned["HeatRisk"] == 0.85
    assert aligned["Humidity"] == 0.65

def test_R3_response_bounds():
    aligned = {"HeatRisk": 1.5, "Humidity": 3.0}
    resp = R3_response(aligned)
    assert resp["HeatRisk"] == 1.5
    assert resp["Humidity"] == 2.0  # bounded
