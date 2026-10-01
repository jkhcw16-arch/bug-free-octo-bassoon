from rpo.projection import project_role

def test_projection_identity():
    exponents = {"HeatRisk": 0.5}
    out = project_role(exponents, rho=1)
    assert out["HeatRisk"] == 2 ** 0.5

def test_projection_rho2():
    exponents = {"HeatRisk": 0.5}
    out = project_role(exponents, rho=2)
    assert out["HeatRisk"] == 2 ** 1.0

def test_projection_monotonicity():
    low = project_role({"HeatRisk": 0.4}, rho=2)["HeatRisk"]
    high = project_role({"HeatRisk": 0.6}, rho=2)["HeatRisk"]
    assert high > low
