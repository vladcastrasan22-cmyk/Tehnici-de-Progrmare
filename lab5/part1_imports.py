# Laborator: funcții, metode și importuri pe web
# Student: Castrașan Vlad
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

    # exerctiul 1
print("Exercitiul 1")
import requests
#print(requests.__version__)
import urllib.request

# requests a avut nevoie de pip install deoarece  requests nu este librarie standarta python dar
# urllib este librarie standarta pyton


    # exercitiul 2
print("Exercitiul 2")
from requests import get
r= requests.get(BASE_URL, timeout=TIMEOUT)
print(r.status_code)
# import requests: avantaj -> claritate, se vede de unde vine funcția și se evită conflictele de nume
# from requests import get: avantaj -> mai puțin de scris, apeluri mai scurte

    # exercitiul 3
print("Exercitiul 3")
import requests as rq
r= rq.get(BASE_URL,timeout=TIMEOUT)
print(r.status_code)
# Alias-ul ajută când e o abreviere standard sau numele e lung (np, pd); încurcă când e obscur (rq) și trebuie să cauți ce înseamnă.

    # exercitiul 4
import urllib.request
import urllib.error
print("Exercitiul 4")
try:
    r= urllib.request.urlopen(BASE_URL, timeout=TIMEOUT)
    raw= r.read()
    a = raw.decode("utf-8")
    print(r.status)
    print(a[:200])
except urllib.error.HTTPError as e:
    print(e.code)
# da eroare deoarece serverul respinge cererile care se prezinta ca Python-urllib/3.14 (antetul User-Agent implicit al lui urllib)

    # exercitiul 5
import requests
print("Exercitiul 5")
print(dir(requests))
print(type(requests.post))
print(type(requests.Response))
#print(type(requests.__build__))

# nume1 cu litera mica -> este o actiune  ( 'post', 'request', 'compat', 'cookies'): de obicei funcții.
# nume2 cu litera mare -> sunt de obicei clase ('Session', 'Response', 'Request'):
# nume3 cu litere mici care sunt un grup de lucruri -> sunt obiecte de module ('__version__','__title__', '__path__'):

    # exercitiul 6
import requests
print("Exercitiul 6")
#help(requests.get)
#help(requests.request)
r= requests.get(BASE_URL,timeout=TIMEOUT)
print(r.status_code)
# Parametrul se numește timeout , numele din documentatie : param timeout :
# Setează timpul maxim de asteptare a raspunsului de la server
# Poate fi un număr sau o pereche (connect timeout, read timeout) unde primul înseamnă cat timp asteptam ca sa stabileasca conexiunea.
# Iar al doilea timpul in care datele sunt trimise dupa stabilirea conexiunii
   
    # exerciul 7
import time
import requests
print("Exercitiul 7")
start= time.perf_counter()
r= requests.get(BASE_URL,timeout=TIMEOUT)
end =time.perf_counter()
durata = end - start
print(durata)
print(r.elapsed.total_seconds())
# perf_counter e mai mare, pentru ca masoara intreg apelul requests.get, iar elapsed doar de la trimiterea cererii pana la primirea antetelor.

    # exercitiul 8
import requests
print("Exercitiul 8")
try:
   # import bs4
    print("bs4 este intalat")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
print(requests.__file__)

