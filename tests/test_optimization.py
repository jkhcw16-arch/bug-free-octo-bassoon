from rpo.optimization import select_least_intrusive

def test_least_intrusive_selection():
    actions = [
        {"action": "A", "intrusion": 0.6, "protection": 0.8},
        {"action": "B", "intrusion": 0.3, "protection": 0.8},
    ]
    chosen = select_least_intrusive(actions, P_min=0.7)
    assert chosen["action"] == "B"

def test_adequacy_constraint():
    actions = [{"action": "A", "intrusion": 0.3, "protection": 0.6}]
    try:
        select_least_intrusive(actions, P_min=0.7)
        assert False
    except ValueError:
        assert True
