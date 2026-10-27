import re
import base64
import hashlib
import argparse
import json
from pathlib import Path
from urllib.parse import unquote


def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"


def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()


def citibil(b):
    return all(32 <= c < 127 for c in b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("intrare", help="text de decodat sau cale fisier")
    parser.add_argument("--fisier", action="store_true", help="trateaza intrarea ca fisier")
    args = parser.parse_args()

    director_lab = Path(__file__).resolve().parents[2]
    director_probe = director_lab / "probe"

    # A1
    s = "Salut"
    b = s.encode()
    print(b, b[0])
    print(b.hex())
    b2 = bytes.fromhex(b.hex())
    print(b2)

    # A2
    print(ghici_strat("%2Fetc"))
    print(ghici_strat("48656c6c6f"))
    print(ghici_strat("U2FsdXQ="))

    # A3
    print(desfa("U2FsdXQ="))
    print(desfa("48656c6c6f"))

    # A4
    val = "NTM1OTU3NTk="
    for _ in range(8):
        strat, b = desfa(val)
        if citibil(b):
            print(b)
            break
        else:
            val = b.decode()

    # A5
    with open(director_probe / "xor.bin", "rb") as fisier:
        date = fisier.read()
    for k in range(256):
        clar = bytes(x ^ k for x in date)
        if citibil(clar):
            print("cheie:", k, clar.decode())

    # A6
    with open(director_probe / "hashuri.txt", encoding="ascii") as fisier:
        hashuri = fisier.readlines()
    with open(director_probe / "wordlist.txt", encoding="latin1") as fisier:
        cuvinte = fisier.readlines()
    for linie_hash in hashuri:
        tinta = linie_hash.strip()
        for linie_cuv in cuvinte:
            cuv = linie_cuv.strip()
            if hashlib.md5(cuv.encode()).hexdigest() == tinta:
                print("gasit:", tinta, "->", cuv)
                break

    if args.fisier:
        with open(args.intrare, "rb") as fisier:
            date2 = fisier.read()
        strat7 = "fisier_binar"
        rezultat_text = date2.hex()
    else:
        strat7, b7 = desfa(args.intrare)
        rezultat_text = b7.decode(errors="replace")

    rezultat = {"strat": strat7, "rezultat": rezultat_text}
    with open(director_lab / "fisa.json", "w", encoding="utf-8") as f:
        json.dump(rezultat, f, indent=2)

    print(rezultat)