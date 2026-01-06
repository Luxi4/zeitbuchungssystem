import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
pfad_users = BASE_DIR / "data" / "userdata.json"
pfad_arbeitsberichte = BASE_DIR / "data" / "arbeitsberichte.json"


class UserData:
    def __init__(self, username, email, password, role="einfach", vip_request=False, admin_request=False):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.vip_request = vip_request
        self.admin_request = admin_request

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "vip_request": self.vip_request,
            "admin_request": self.admin_request,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role", "einfach"),
            vip_request=data.get("vip_request", False),
            admin_request=data.get("admin_request", False),
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
    def __init__(self, username, modul, datum, minuten, inhalt):
        self.username = username
        self.modul = modul
        self.datum = datum
        self.minuten = minuten
        self.inhalt = inhalt

    def to_dict(self):
        return {
            "username": self.username,
            "modul": self.modul,
            "datum": self.datum,
            "minuten": self.minuten,
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
def zeit_pro_modul(username):
    with open (pfad_arbeitsberichte, "r", encoding="utf-8") as f:
        daten = json.load(f)

        summen = {}

        for eintrag in daten:
            if eintrag.get("username") == username:
                modul = eintrag["modul"]
                minuten = eintrag["minuten"]

                if modul not in summen:
                    summen[modul] = 0
            
                summen[modul] += minuten

        return summen

def prozentanteile(username):
    summen = zeit_pro_modul(username)

    if not summen:
        return []
    
    gesamt = 0
    for modul in summen:
        gesamt = gesamt + summen[modul]
    
    ergebnis = []
    for modul in summen:
        minuten = summen[modul]
        prozent = round(minuten / gesamt * 100, 2)

        eintrag = {
            "modul": modul,
            "minuten": minuten,
            "prozent": prozent
        }

        ergebnis.append(eintrag)
    
    return ergebnis