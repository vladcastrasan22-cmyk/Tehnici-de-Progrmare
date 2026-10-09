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

DEFAULT_HEADERS = {"User-Agent": "WebLab-Castrasan Vlad"} 


def get_status(url):
    r= requests.get(url,timeout=TIMEOUT)
    return r.status_code


def fetch(url, timeout=10):
    r= requests.get(url,timeout=timeout, headers=DEFAULT_HEADERS)
    return r


def get_title(html):
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    return title

def check_paths(base, paths):
    rezultat = {}
    for cale in paths:
        url_complet = base + cale
        r = requests.get(url_complet,timeout=TIMEOUT)
        rezultat[cale] = r.status_code
        time.sleep(1)
    return rezultat

def extract_links(html):
    legaturi = re.findall(r'href="([^"]+)"', html)
    return sorted(set(legaturi))
r = requests.get(BASE_URL, timeout=TIMEOUT)
unice = extract_links(r.text)

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

def page_fingerprint(url):
    r = requests.get(url, timeout=TIMEOUT)
    h = hashlib.sha256(r.content).hexdigest()
    return h

def resolve(hostname):
    socket.gethostbyname(hostname)
    return socket.gethostbyname(hostname)


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


def get_header(url, name, default="lipsește"):
    r = requests.get(BASE_URL, timeout=TIMEOUT)
    return r.headers.get(name, default)


def score_headers(results: dict[str, bool]) -> str:
    found = sum(results.values())
    total = len(results)
    return f"{found}/{total}"

def fetch_robots(base):
    r = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    if r.status_code == 200:
        return r.text
    return None


def disallowed_paths(robots_text):
    if robots_text is None:
        return []

    values = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                values.append(value)
    return values

def response_times(*urls):
    url_dict = {}
    for url in url_dict:
        time.sleep(1)
        r =requests.get(url, timeout=TIMEOUT)
        total_time = r.elapsed.total_seconds()
        url_dict[url] = total_time
    return url_dict



def site_report(url):
    print(f"=== Raport site: {url} ===")
    
    # 1. Cod de stare și URL final
    r = fetch(url)
    status_code = r.status_code
    
    # 2. Titlu
    title = get_title(r.text)
    
    # Extragem domeniul pentru funcțiile care necesită doar hostname-ul
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.netloc
    base_domain = f"{parsed_url.scheme}://{hostname}"
    
    # 3. Adresa IP
    ip_address = resolve(hostname)
    
    # 4. Lanțul de redirecționări de la http://
    http_url = url.replace("https://", "http://")
    r_http = requests.get(http_url, timeout=TIMEOUT)
    redirects = []
    for resp in r_http.history:
        redirects.append(f"{resp.status_code} -> {resp.url}")
        
    # 5. Scorul antetelor de securitate
    headers_to_check = [
        "Strict-Transport-Security", "Content-Security-Policy", 
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
    ]
    sec_results = {}
    for h in headers_to_check:
        sec_results[h] = h in r.headers
    sec_score = score_headers(sec_results)
    
    # 6. Zile până la expirarea certificatului
    days_left = cert_days_left(hostname)
    
    # 7. Numărul de legături interne și externe
    toate_legaturile = extract_links(r.text)
    interne, externe = split_links(toate_legaturile, hostname)
    
    # 8. Căile interzise din robots.txt
    robots_text = fetch_robots(base_domain)
    cai_interzise = disallowed_paths(robots_text)
    
    # --- AFIȘARE ÎN CONSOLĂ ---
    print(f"Cod de stare:      {status_code}")
    print(f"Titlu:             {title}")
    print(f"Adresă IP:         {ip_address}")
    
    print("Redirecționări:   ")
    if redirects:
        for red in redirects:
            print(f"   {red}")
    else:
        print("   Nicio redirecționare")
        
    print(f"Scor securitate:   {sec_score}")
    print(f"Certificat:        {days_left} de zile rămase")
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    
    cai_str = ", ".join(cai_interzise) if cai_interzise else "Niciuna"
    print(f"Căi interzise:     {cai_str}")
    
    # --- SALVARE ÎN JSON ---
    date_json = {
        "url": url,
        "status_code": status_code,
        "title": title,
        "ip_address": ip_address,
        "redirects": redirects,
        "security_score": sec_score,
        "certificate_days_left": days_left,
        "links": {
            "internal": len(interne),
            "external": len(externe)
        },
        "disallowed_paths": cai_interzise
    }
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(date_json, f, indent=4, ensure_ascii=False)
        
    print("Salvat în report.json")


    
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
