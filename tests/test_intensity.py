from rpo.intensity import map_intensities

def test_intensity_bounds():
    projected = {"HeatRisk": 100.0}
    intensities = map_intensities(projected)
    assert 0.0 <= intensities["HeatRisk"] <= 1.0

def test_intensity_monotonicity():
    low = map_intensities({"HeatRisk": 10.0})["HeatRisk"]
    high = map_intensities({"HeatRisk": 20.0})["HeatRisk"]
    assert high > low
