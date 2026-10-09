import time
import requests
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

    # exercitiul 21
#print("Exercitiul 21")
#def fetch(url):
#    r= requests.get(url,timeout=TIMEOUT)
#    return r
#raspuns = fetch(BASE_URL)
#print(raspuns.status_code)

    # exercitiul 22
print("Exercitiul 22")
def get_status(url):
    r= requests.get(url,timeout=TIMEOUT)
    return r.status_code
raspuns = get_status(BASE_URL + "/")
print(raspuns)
time.sleep(1)
raspuns = get_status(BASE_URL +  "/robots.txt")
print(raspuns)
time.sleep(1)
raspuns = get_status(BASE_URL + "/sitemap.xml")
print(raspuns)

    # exercitiul 23
print("Exercitiul 23")
def fetch(url, timeout=10):
    r= requests.get(url,timeout=timeout)
    return r
raspuns = fetch(BASE_URL)
print(raspuns.status_code)
time.sleep(1)
raspuns = fetch(BASE_URL,timeout=3)
print(raspuns.status_code)

    # exercitiul 24
#print("Exercitiul 24")
#def get_title(html):
#    start = html.find("<title>") + len("<title>")
#    end = html.find("</title>")
#    title = html[start:end].strip()
#    return title
#r = fetch(BASE_URL, timeout=TIMEOUT)
#html = r.text
#print(get_title(html))

    # exercitiul 25
print("Exercitiul 25")
def get_title(html):
    """ functie utilizata pentru preluarea titlului """
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    return title
r = fetch(BASE_URL, timeout=TIMEOUT)
html = r.text
print(get_title(html))
help(get_title)

    # exercitiul 26
#print("Exercitiul 26")
#def get_status(url: str) -> int:
#   r= requests.get(url,timeout=TIMEOUT)
#    return r.status_code
# get_status(123)
# Răspuns: Nu, adnotările de tip nu opresc execuția codului în Python. Ele sunt doar informative.
# Eroarea apare abia în interiorul funcției, deoarece requests.get() nu acceptă un număr în loc de URL.

    # exercitiul 27
print("Exercitiul 27")
def page_exists(url):
    try:
        r = requests.get(url,timeout=TIMEOUT)
    except requests.RequestException:
        return False
    return True
print(page_exists("https://this-domain-does-not-exist.invalid"))

    # exercitiul 28
print("Exercitiul 28")
def check_paths(base, paths):
    rezultat = {}
    for cale in paths:
        url_complet = base + cale
        r = requests.get(url_complet,timeout=TIMEOUT)
        rezultat[cale] = r.status_code
        time.sleep(1)
    return rezultat
print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

    # exercitiul 29
print("Exercitiul 29")
def get_header(url, name, default="lipsește"):
    r = requests.get(url, timeout=TIMEOUT)
    return r.headers.get(name, default)
print(get_header(BASE_URL, name="Server"))

    # exercitiul 30
print("Exercitiul 30")
SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def security_headers(url: str) -> dict[str, bool]:
    r = requests.get(url, timeout=TIMEOUT)
    return {header: header in r.headers for header in SECURITY_HEADERS}

dictionar_rezultate = security_headers(BASE_URL)
print(dictionar_rezultate)

    # exercitiul 31
print("Exercitiul 31")
def score_headers(results: dict[str, bool]) -> str:
    found = sum(results.values())
    total = len(results)
    return f"{found}/{total}"

print(score_headers(security_headers(BASE_URL)))

    # exercitiul 32
print("Exercitiul 32")
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


robots_text = fetch_robots(BASE_URL)
print(disallowed_paths(robots_text))
print(disallowed_paths(None))   # test: trebuie să afișeze []


    # exercitiul 33
print("Exercitiul 33")
def response_times(*urls):
    url_dict = {}
    for url in url_dict:
        time.sleep(1)
        r =requests.get(url, timeout=TIMEOUT)
        total_time = r.elapsed.total_seconds()
        url_dict[url] = total_time
    return url_dict
my_get = response_times(BASE_URL, ECHO_URL)
print(my_get)


    # exercitiul 34
print("Exercitiul 34")
def log(message, **details):
    final_message = message
    for key, value in details.items():
        final_message += f" | {key}={value}"
    print(final_message)
print(log("verificat", url=BASE_URL, status=200))
