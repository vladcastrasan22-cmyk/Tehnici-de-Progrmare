from dataclasses import dataclass, asdict
import json
 
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str
 
p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)