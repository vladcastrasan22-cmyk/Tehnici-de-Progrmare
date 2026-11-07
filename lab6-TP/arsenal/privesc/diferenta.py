from pathlib import Path
from arsenal.privesc.enum import citeste_linii, nume, GTFO

def cai(fisier):
    return set(citeste_linii(fisier))

# B1
start = Path(__file__).parent / "start"

baza = cai(start / "baza_suid.txt")
acum = cai(start / "suid.txt")

print("baza:", len(baza), " acum:", len(acum))

# B2
noi = acum - baza
print(f"{len(noi)} SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)

# B3
risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
print("periculoase NOI:", periculoase)

