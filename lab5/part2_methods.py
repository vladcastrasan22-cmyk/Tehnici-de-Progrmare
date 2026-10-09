# Laborator: funcții, metode și importuri pe web
# Student: Castrașan Vlad

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

    # exercitiul 9
print("Exercitiul 9")
import requests
r= requests.get(BASE_URL,timeout=TIMEOUT)
print(r.status_code) # atribut
print(r.ok) # atribut
print(r.url) # atribut
print(r.encoding) # atribut
print(callable(r.status_code))
print(callable(r.ok))
print(callable(r.url))
print(callable(r.encoding))

    # exercitiul 10

import requests
print("Exercitiul 10")
try:
    print(r.ok)
    r = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    r.raise_for_status()
except requests.HTTPError as e:
    print(e)

    # exercitiul 11
import requests
print("Exercitiul 11")
r = requests.get(BASE_URL, timeout=TIMEOUT)
antet= r.headers.items()
for nume,valoare in antet:
    print(f'{nume}<:>{valoare}')

    # exercitiul 12
import requests
print("Exercitiul 12")
r = requests.get(BASE_URL, timeout=TIMEOUT)
print(r.headers.get("Server", "lipseste"))
print(r.headers.get("Content-type", "lipseste"))
print(r.headers.get("content-type"))
## Rezultat identic: antetele HTTP nu sunt case sensitive, iar response.headers ține cont de asta.

    # exercitiul 13
import requests
print("Exercitiul 13")
r = requests.get(BASE_URL, timeout=TIMEOUT)
titlu = r.text.lower().count("cyber")
print(titlu) # Se pot inlantui pentru ca .lower() returneaza tot sirul cu litere mici, iar pe acesta se poate apela functia .count()

    # exercitiul 14
import requests
print("Exercitiul 14")
r = requests.get(BASE_URL, timeout=TIMEOUT)
html = r.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
title = html[start:end].strip()
print(title)

    # exercitiul 15
import requests
print("Exercitiul 15")
r = requests.get(BASE_URL, timeout=TIMEOUT)
linii = r.text.splitlines()
print(len(html))
print(len(max(linii, key=len)))

    # exrcitiul 16
import requests
print("Exercitiul 16")
r = requests.get(BASE_URL, timeout=TIMEOUT)
if r.url.startswith("https://"):
    print("conexiune securizata")
else:
    print("conexiune nesecurizata")

    # exercitiul 17
import requests
print("Exercitiul 17")
r = requests.get("http://cybercor.org", timeout=TIMEOUT)
for variabila in r.history:
    print(variabila.status_code)
    print(variabila.url)
print("url final: " + r.url )

    # exercitiul 18
import requests,time
print("Exercitiul 18")
g = requests.get(BASE_URL, timeout=TIMEOUT) # get() Descarcă tot conținutul paginii sau fișierului.
time.sleep(1)
h = requests.head(BASE_URL, timeout=TIMEOUT) # head() Descarcă doar metadatele (dimensiune, tip fișier): este 0, pentru că serverul la HEAD trimite doar antetele, fără corp, deci .content este gol
print(len(g.content))
print(len(h.content))

    # exercitiul 19
import requests
print("Exercitiul 19")
r = requests.get(BASE_URL, timeout=TIMEOUT)
if len(r.cookies) ==0 :
    print("Niciun cookie setat")
for a in r.cookies:
    print(f"{a.name}: {a.secure}")

    # exercitiul 20
import requests
print("Exercitiul 20")
sesiune= requests.Session()
sesiune.headers.update({"User-Agent": "WebLab-Castrasan Vlad"})
r= sesiune.get(ECHO_URL + "/headers",timeout=TIMEOUT)
print(r.text)
print(r.json())
# .text este atribut (un sir de caractere), iar .json() este metoda care parseaza textul JSON si returneaza un dictionar Python, in care pot accesa chei.