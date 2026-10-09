# Laborator: funcții, metode și importuri pe web
# Student: Castrașan Vlad
 
#BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import webtools
from webtools import get_status, fetch, get_title, check_paths, site_report
from webtools import get_title # security_headers
from webtools import fetch, DEFAULT_HEADERS
import argparse
import csv
from datetime import datetime

parser = argparse.ArgumentParser(description="python main.py https://cybercor.org")
parser.add_argument("url", help="python main.py https://cybercor.org")
args = parser.parse_args()



    # exercitiul 44
print("Exercitiul 44")
print(webtools.get_title(webtools.fetch(args.url).text))

    # exercitiul 45
print("Exercitiul 45")    
# Dacă main.py ar avea propria sa funcție numită get_title, ar apărea o coliziune de nume.
# Ultima funcție definită sau importată în cod o va suprascrie pe cealaltă. 
# De exemplu, dacă importul este la început, iar funcția locală este definită mai jos, 
# funcția importată va fi anulată și se va executa doar cea locală.

    # exercitiul 46
print("Exercitiul 46")
# Autotestul rulează doar când pornim direct webtools.py pentru că atunci Python 
# setează variabila internă __name__ la valoarea "__main__". 
# Când rulăm main.py, fișierul webtools.py este doar importat. În acest caz, 
# __name__ devine "webtools", condiția este falsă, iar testul este ignorat.

    # exercitiul 47
print("Exercitiul 47")
print(DEFAULT_HEADERS)


    # exercitiul 48
print("Exercitiul 48")
print(args.url)

    # exercitiul 49
print("Exercitiul 49")
rezultate_paths = check_paths(args.url, ["/", "/robots.txt", "/sitemap.xml"])
with open("report.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["path", "status", "checked_at"])  # Corectat capul de tabel
    for cale, status in rezultate_paths.items():
        writer.writerow([cale, status, datetime.now().isoformat()]) 
print("Rezultatele au fost salvate în report.csv")



print("Exercitiul 50")
site_report(args.url)