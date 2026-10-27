import re
from pathlib import Path

from PIL import Image


def tip_real(cale):
    with open(cale, "rb") as fisier:
        cap = fisier.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    else:
        return cap.hex()


def extrage_texte(cale):
    with open(cale, "rb") as fisier:
        date = fisier.read()
    return [m.decode() for m in re.findall(rb"[ -~]{4,}", date)]


def extrage_gps(cale):
    with Image.open(cale) as imagine:
        exif = imagine.getexif()
        gps = exif.get_ifd(34853)
        if not gps:
            return None

        lat_dms, lat_ref = gps[2], gps[1]
        lon_dms, lon_ref = gps[4], gps[3]

    lat = float(lat_dms[0]) + float(lat_dms[1]) / 60
    lat += float(lat_dms[2]) / 3600
    lon = float(lon_dms[0]) + float(lon_dms[1]) / 60
    lon += float(lon_dms[2]) / 3600

    if isinstance(lat_ref, bytes):
        lat_ref = lat_ref.decode("ascii")
    if isinstance(lon_ref, bytes):
        lon_ref = lon_ref.decode("ascii")

    if lat_ref == "S":
        lat = -lat
    if lon_ref in ("V", "W"):
        lon = -lon
    return lat, lon


def carving_zip(cale, iesire="gasit.zip"):
    with open(cale, "rb") as fisier:
        date = fisier.read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None
    with open(iesire, "wb") as f:
        f.write(date[i:])
    return i


def ascunde_lsb(cale_sursa, mesaj, cale_iesire="stego.png"):
    with Image.open(cale_sursa) as imagine:
        img = imagine.convert("RGB")
    px = list(img.getdata())
    mesaj = mesaj + b"\x00"         
    biti = "".join(f"{x:08b}" for x in mesaj)

    if len(biti) > len(px):
        raise ValueError(
            f"Mesajul este prea mare: {len(biti)} biti disponibili, "
            f"dar imaginea poate stoca doar {len(px)}"
        )

    px_nou = []
    for i, (r, g, b) in enumerate(px):
        if i < len(biti):
            bit = int(biti[i])
            r = (r & ~1) | bit
        px_nou.append((r, g, b))

    img.putdata(px_nou)
    img.save(cale_iesire)


def dezvaluie_lsb(cale):
    with Image.open(cale) as imagine:
        px = list(imagine.convert("RGB").getdata())
    biti = "".join(str(r & 1) for (r, g, b) in px)
    octeti = []
    for i in range(0, len(biti), 8):
        octet = biti[i:i + 8]
        if len(octet) < 8:
            break
        valoare = int(octet, 2)
        if valoare == 0:
            break
        octeti.append(valoare)

    return "".join(chr(o) for o in octeti)


if __name__ == "__main__":
    director_lab = Path(__file__).resolve().parents[2]
    director_probe = director_lab / "probe"

    # B1
    print(tip_real(director_probe / "foto.jpg"))
    print(tip_real(director_probe / "ascuns.png"))

    # B2
    for linie in extrage_texte(director_probe / "ascuns.png"):
        print(linie)

    # B3
    rezultat_gps = extrage_gps(director_probe / "foto.jpg")
    if rezultat_gps:
        lat, lon = rezultat_gps
        print("Latitudine:", lat)
        print("Longitudine:", lon)

    # B4
    poz = carving_zip(director_probe / "ascuns.png", director_lab / "gasit.zip")
    if poz is not None:
        print("arhiva extrasa de la octetul", poz)

    # B5
    cale_stego = director_lab / "stego.png"
    ascunde_lsb(director_probe / "foto.jpg", b"FLAG{ascuns_in_pixeli}", cale_stego)

    # B6
    mesaj_gasit = dezvaluie_lsb(cale_stego)
    print("mesaj dezvaluit:", mesaj_gasit)
