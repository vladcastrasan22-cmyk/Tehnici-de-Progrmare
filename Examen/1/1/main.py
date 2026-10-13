import requests
TIMEOUT = 5

from checker import build_url, is_https, show_response
import checker

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




 #1
print(build_url("example.com", "/login"))  
print(is_https("https://example.com"))  
print(is_https("http://this-site-does-not-exist.invalid"))  

#2
print(show_response("https://example.com"))

#3
print(checker.check_site("https://example.com"))  
print(checker.check_site("https://httpbin.org/html"))
print(checker.check_site("https://httpbin.org/status/200"))
print(checker.check_site("https://httpbin.org/redirect/1"))
print(checker.check_site("https://httpbin.org/delay/2"))
print(checker.check_site("https://httpbin.org/status/404"))
print(checker.check_site("https://httpbin.org/status/500"))
print(checker.check_site("https://httpbin.org/delay/10"))
print(checker.check_site("https://httpbin.org/delay/10"))
print(checker.check_site("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print(checker.check_site("https://httpbin.org/response-headers?x-frame-options=DENY"))
print(checker.check_site("https://httpbin.org/status/200,500"))
    


#4
print(checker.scan_sites("https://example.com"))  
print(checker.scan_sites("https://httpbin.org/html"))
print(checker.scan_sites("https://httpbin.org/status/200"))
print(checker.scan_sites("https://httpbin.org/redirect/1"))
print(checker.scan_sites("https://httpbin.org/delay/2"))
print(checker.scan_sites("https://httpbin.org/status/404"))
print(checker.scan_sites("https://httpbin.org/status/500"))
print(checker.scan_sites("https://httpbin.org/delay/10"))
print(checker.scan_sites("https://httpbin.org/delay/10"))
print(checker.scan_sites("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print(checker.scan_sites("https://httpbin.org/response-headers?x-frame-options=DENY"))
print(checker.scan_sites("https://httpbin.org/status/200,500"))


#5
print(checker.check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY"))


#6
print(checker.retry_check("https://httpbin.org/status/200,500", attempts=3))
