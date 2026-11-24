import os, hashlib
MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}
 
def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"
 
print(tip(b"\x89PNG\r\n"), tip(b"%PDF-1.4"), tip(b"text"))


def amprenta_fisier(cale):
    with open(cale, "rb") as f:      # "rb" = binar; with = inchide singur
        date = f.read()
    return {"nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]}
 
print(amprenta_fisier("arsenal/forensics/probe/imagine.png"))