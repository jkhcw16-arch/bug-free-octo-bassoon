# projection.py

def test_monotonicity(cat, alpha_low, alpha_high, rho):
    low = project_role({cat: alpha_low}, rho)[cat]
    high = project_role({cat: alpha_high}, rho)[cat]
    return high > low
