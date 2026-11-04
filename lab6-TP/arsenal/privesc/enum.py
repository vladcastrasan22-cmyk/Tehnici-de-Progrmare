import argparse, json, os

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        linii = [line.strip() for line in f]
        return [line for line in linii if line and not line.startswith("#")]

cai = citeste_linii("arsenal/privesc/start/suid.txt")
print("linii SUID:", len(cai))


def nume(cale):
    # TODO: intoarce ce e dupa ultimul "/"  (vezi rsplit)
    ...
    return cale.rsplit("/", 1)[-1]
 
nume_unice = {nume(c) for c in cai}    # set comprehension
print("SUID distincte:", len(nume_unice))


def suid_constatari(cale):
    cai = citeste_linii(cale)
    # TODO: pentru fiecare cale UNICA, in ordine sortata, un dict:
    #   {"cale": c, "nume": nume(c),
    #    "risc": "mare" daca nume(c) in GTFO, altfel "normal"}
    return [{"cale": c, "nume": nume(c), "risc": "mare" if nume(c) in GTFO else "normal"} for c in sorted(cai, key=nume)]


suid = suid_constatari("arsenal/privesc/start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))