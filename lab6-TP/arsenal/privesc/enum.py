import argparse, json, os
 
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        linii = [line.strip() for line in f]
        return [line for line in linii if line and not line.startswith("#")]

cai = citeste_linii("arsenal/privesc/start/suid.txt")
print("linii SUID:", len(cai))