import requests

TIMEOUT = 5  
SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    r=requests.get(f"https://{host}{path}",timeout=TIMEOUT)

    return f"https://{host}{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    r=requests.get(url,timeout=TIMEOUT)
    if url.startswith("https://"):
        return True
    elif url.startswith("http://"):
        return False
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url,timeout=TIMEOUT)
    print(f"Status: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}")
    return r.status_code, r.headers.get('Content-Type')

def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    r = requests.get(url,timeout=TIMEOUT)
    status = r.status_code
    content_type = r.headers.get("Content-Type")
    length = len(r.content)
    server = r.headers.get("Server")
    return status, content_type, length, server
    

def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for url in SITES:
        try:
            r = requests.get(url,timeout=TIMEOUT)
            print(f"{url} - Status: {r.status_code}")
            results.append((url, r.status_code))
        except requests.exceptions.RequestException as e:
            print(f"{url} - Error: {e}")
    return results


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    r = requests.get(url,timeout=TIMEOUT)
    dictionary=[]
    for header in SECURITY_HEADERS:
        if header in r.headers:
            present_headers = [header for header in SECURITY_HEADERS if header in r.headers]
            score = len(present_headers) / len(SECURITY_HEADERS) * 100
            dictionary = {
                "present": present_headers,
                "missing": [],
                "score": score,
            }
        else:
            missing_headers = [header for header in SECURITY_HEADERS if header not in r.headers]
    
    return dictionary




def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    r=requests.get(url,timeout=TIMEOUT)
    if attempts >=3:
        return {"status": None, "attempts": 0}
    for attempt in range(attempts):
        try:
            r = requests.get(url,timeout=TIMEOUT)
            return {"status": r.status_code, "attempts": attempt + 1}
        except requests.exceptions.RequestException:
            continue
    return {"status": r.status_code, "attempts": attempts}