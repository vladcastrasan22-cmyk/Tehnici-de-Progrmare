from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        return any(cai in self.cale for cai in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"


p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)
print(p.e_suspect())

e1 = Eveniment(4625, "warning", "Security", "administrator", "An account failed to log on")
e2 = Eveniment(4624, "information", "Security", "ana", "An account was logged on")
print(e1.e_suspect(), e2.e_suspect())


def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce [Proces(**d) for d in json.load(f)]
        return [Proces(**d) for d in json.load(f)]
 
procese = procese_din_json("arsenal/windows/start/procese.json")
print("procese:", len(procese))
print("suspecte:", sum(1 for p in procese if p.e_suspect()))



@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            # TODO: return cls([Proces(**d) for d in json.load(f)])
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
 
inv = Inventar.din_json("arsenal/windows/start/procese.json")
print("procese:", len(inv))