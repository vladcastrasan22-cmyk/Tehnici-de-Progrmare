import sys
sys.path.append("arsenal/forensics")
from decode import desfa

def test_base64():
    strat, rezultat = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert rezultat == b"Salut"

test_base64()
print("Test trecut!")