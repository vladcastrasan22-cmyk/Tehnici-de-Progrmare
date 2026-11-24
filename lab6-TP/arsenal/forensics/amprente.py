import os, hashlib
import argparse
MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}
 
def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"
 


def amprenta_fisier(cale):
    with open(cale, "rb") as f:      # "rb" = binar; with = inchide singur
        date = f.read()
    return {"nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]}
 


def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez
 

def main():
    parser = argparse.ArgumentParser(description="Scanează un folder și afișează amprentele fișierelor.")
    parser.add_argument("folder", help="Folderul de scannat")
    args = parser.parse_args()

    rez = scaneaza(args.folder)
    for f in rez:
        print(f"{f['nume']:14} {f['tip']:11} {f['sha256']}")

if __name__ == "__main__":
    main()

