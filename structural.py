# structural.py

def test_prime_uniqueness(prime_table):
    return len(set(prime_table.values())) == len(prime_table.values())
