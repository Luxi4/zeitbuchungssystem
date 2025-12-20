import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
pfad_users = BASE_DIR / "data" / "userdata.json"
pfad_arbeitsberichte = BASE_DIR / "data" / "arbeitsberichte.json"


class UserData:
    def __init__(self, username, email, password, role="einfach"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role", "einfach"),
        )

def load_users():
    if pfad_users.exists():
        with pfad_users.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [UserData.from_dict(obj) for obj in data]
    return []

def save_users(users):
    with pfad_users.open("w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=4, ensure_ascii=False)



class Arbeitsberichte:
    def __init__(self, modul, datum, min, inhalt):
        self.modul = modul
        self.datum = datum
        self.min = min
        self.inhalt = inhalt

    def to_dict(self):
        return {
            "modul": self.modul,
            "datum": self.datum,
            "min": self.min,
            "inhalt": self.inhalt,
        }

def lade_berichte():
    try:
        with open (pfad_arbeitsberichte, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def speichere_berichte(berichte):
    with open(pfad_arbeitsberichte, "w", encoding="utf-8") as f:
        json.dump(berichte, f, indent=2, ensure_ascii=False)


#gesamtübersicht
def zeit_pro_modul():
    with open (pfad_arbeitsberichte, "r", encoding="utf-8") as f:
        daten = json.load(f)

        summen = {}
        for eintrag in daten:
            modul = eintrag["modul"]
            minuten = eintrag["minuten"]

            if modul not in summen:
                summen[modul] = 0
            
            summen[modul] += minuten

    return summen

def prozentanteile():
    summen = zeit_pro_modul()
    gesamt = 0

    for modul in summen:
        gesamt = gesamt + summen[modul]
    
    ergebnis = []
    for modul in summen:
        minuten = summen[modul]
        prozent = minuten / gesamt * 100
        ergebnis.append({
            "modul": modul,
            "minuten": minuten,
            "prozent": prozent
        })
    
    return ergebnis