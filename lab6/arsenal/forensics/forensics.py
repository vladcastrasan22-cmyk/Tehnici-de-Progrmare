import re
from PIL import Image
from PIL.ExifTags import TAGS


def tip_real(cale):
    cap = open(cale, "rb").read(8)
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
    date = open(cale, "rb").read()
    return [m.decode() for m in re.findall(rb"[ -~]{4,}", date)]


def extrage_gps(cale):
    exif = Image.open(cale)._getexif() or {}
    if 34853 not in exif:
        return None
    gps = exif[34853]
    lat_dms, lat_ref = gps[2], gps[1]
    lon_dms, lon_ref = gps[4], gps[3]

    lat = float(lat_dms[0] + lat_dms[1] / 60 + lat_dms[2] / 3600)
    lon = float(lon_dms[0] + lon_dms[1] / 60 + lon_dms[2] / 3600)

    if lat_ref == "S":
        lat = -lat
    if lon_ref in ("V", "W"):
        lon = -lon
    return lat, lon


def carving_zip(cale, iesire="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None
    with open(iesire, "wb") as f:
        f.write(date[i:])
    return i


def ascunde_lsb(cale_sursa, mesaj, cale_iesire="stego.png"):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())
    mesaj = mesaj + b"\x00"          # terminator, esential pentru B6
    biti = "".join(f"{x:08b}" for x in mesaj)

    px_nou = []
    for i, (r, g, b) in enumerate(px):
        if i < len(biti):
            bit = int(biti[i])
            r = (r & ~1) | bit
        px_nou.append((r, g, b))

    img.putdata(px_nou)
    img.save(cale_iesire)


def dezvaluie_lsb(cale):
    px = list(Image.open(cale).convert("RGB").getdata())
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
    # B1
    print(tip_real("probe/foto.jpg"))
    print(tip_real("probe/ascuns.png"))

    # B2
    for linie in extrage_texte("probe/ascuns.png"):
        print(linie)

    # B3
    rezultat_gps = extrage_gps("probe/foto.jpg")
    if rezultat_gps:
        lat, lon = rezultat_gps
        print("Latitudine:", lat)
        print("Longitudine:", lon)

    # B4
    poz = carving_zip("probe/ascuns.png")
    if poz is not None:
        print("arhiva extrasa de la octetul", poz)

    # B5
    ascunde_lsb("probe/foto.jpg", b"FLAG{ascuns_in_pixeli}")

    # B6
    mesaj_gasit = dezvaluie_lsb("stego.png")
    print("mesaj dezvaluit:", mesaj_gasit)