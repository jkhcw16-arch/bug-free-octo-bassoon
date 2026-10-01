# optimization.py

def test_least_intrusive(actions, P_min):
    chosen = select_least_intrusive(actions, P_min)
    return chosen["intrusion"] == min(a["intrusion"] for a in actions if a["protection"] >= P_min)
