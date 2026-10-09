# Laborator: funcții, metode și importuri pe web
# Student: Castrasan Vlad
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
from pydoc import html
import socket
import time
import requests
import urllib.parse
import urllib
import re
import hashlib
import json
import ssl
import socket
import contextlib


    #exercitiul 35
print("Exercitiul 35")
r = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print(r.scheme)
print(r.netloc)
print(r.path)
print(r.query)
print(r.fragment)

    #exercitiul 36
print("Exercitiul 36")
index=("/about","contact.html","../index.html")
for i in index:
    print(f"{i} -> {urllib.parse.urljoin(BASE_URL, i)}")

    #exercitiul 37
def extract_links(html):
    legaturi = re.findall(r'href="([^"]+)"', html)
    return sorted(set(legaturi))
r = requests.get(BASE_URL, timeout=TIMEOUT)
unice = extract_links(r.text)
print(unice)
print(len(unice))

    # exercitiul 38
print("Exercitiul 38")
def split_links(links, domain):
    same_domain = []
    other_domains = []
    base = "https://" + domain          # baza se construieste din parametru, o singura data
    for link in links:
        absolute_link = urllib.parse.urljoin(base, link)
        netloc = urllib.parse.urlparse(absolute_link).netloc
        if netloc.lower() == domain.lower():
            same_domain.append(absolute_link)
        else:
            other_domains.append(absolute_link)
    return same_domain, other_domains
print(split_links(unice, "cybercor.org"))

    #exercitiul 39
print("Exercitiul 39")
from html.parser import HTMLParser

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
 
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)
finder = ImageFinder()
finder.feed(test_html)
print(finder.images)
 
assert finder.images == [
    "/logo.png",                            # imagine obișnuită
    "poza.jpg",                             # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")        

finder = ImageFinder()
finder.feed(r.text)
for src in finder.images:
    print(src)

    #exercitiul 40
print("Exercitiul 40")
def page_fingerprint(url):
    r = requests.get(url, timeout=TIMEOUT)
    h = hashlib.sha256(r.content).hexdigest()
    return h
a = page_fingerprint(BASE_URL)
time.sleep(1)
b = page_fingerprint(BASE_URL)
print(a)
print(b)
if a == b:
    print("Ambele amprente sunt identice")
else:
    print("Ambele amprente sunt diferite")
# Amprentele sunt identice, pentru ca pagina este statica: serverul trimite aceiasi octeti la fiecare cerere.
# Ar fi diferite daca s-ar schimba macar un octet intre cereri: o data sau ora afisata, un contor, un token generat la fiecare cerere, reclame, sau servere diferite in spatele aceluiasi site.

    # exercitiul 41
print("Exercitiul 41")
r = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w") as file:
    json.dump(dict(r.headers), file, indent=2)
with open("headers.json", "r") as file:
    incarcat = json.load(file)
vizibil = incarcat.get("Content-Type", "N/A")
print(vizibil)

    # exercitiul 42
print("Exercitiul 42")
def resolve(hostname):
    socket.gethostbyname(hostname)
    return socket.gethostbyname(hostname)
ip = resolve(BASE_URL.replace("https://", ""))
print(ip)

    # exercitiul 43
print("Exercitiul 43")
def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as wrapped_sock:
            certificate = wrapped_sock.getpeercert()
            if certificate is None:
                raise ssl.SSLError("Peer certificate is unavailable")
            not_after = certificate.get("notAfter")
            if not isinstance(not_after, str):
                raise ssl.SSLError("Peer certificate is missing a valid notAfter value")
            expiry = ssl.cert_time_to_seconds(not_after)
    return int((expiry - time.time()) / (24 * 60 * 60))
print(cert_days_left(BASE_URL.replace("https://", "")))
