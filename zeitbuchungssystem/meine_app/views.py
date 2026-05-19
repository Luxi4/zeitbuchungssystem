from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from pathlib import Path

from .user_data import UserData, from_dict


BASE_DIR = Path(__file__).resolve().parent
pfad_users = BASE_DIR / "data" / "userdata.json"
pfad_arbeitsberichte = BASE_DIR / "data" / "arbeitsberichte.json"
pfad_modules = BASE_DIR / "data" / "modules.json"


def home(request):
    return render(request, "meine_app/home.html")


#REGISTRIERUNGS-BEREICH



def load_users():
    if pfad_users.exists():
        with pfad_users.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [from_dict(obj) for obj in data]
    return []

def save_users(users):
    with pfad_users.open("w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=4, ensure_ascii=False)

#REGISTRIERUNG
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        users = load_users()

        #Prüfen, ob E-Mail schon existiert
        for u in users:
            if u.email == email:
                return render(request, "meine_app/register.html", {"error": "E-Mail ist bereits registriert!"})

        if users:
            new_id = users[-1].id + 1
        else:
            new_id = 1

        new_user = UserData(
            username=username,
            email=email,
            password=password,
            role="einfach",
            user_id=new_id,
            is_active=True
        )

        users.append(new_user)
        save_users(users)

        #benutzer nach registrierung automatisch einloggen

        return redirect(f"/arbeitsberichte?user_id={new_id}")
    
    return render(request, "meine_app/register.html")


#LOGIN
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        users = load_users()

        for u in users:
            if u.email == email and u.password == password:
                
                if u.is_active == False:
                    return render(request, "meine_app/login.html", {
                        "error": "Benutzer ist gesperrt! Wende dich an einen Administrator."
                    })
                
                return redirect(f"/arbeitsberichte?user_id={u.id}")
        
        return render(request, "meine_app/login.html", {"error": "Login fehlgeschlagen!"})
    
    return render(request, "meine_app/login.html")

#LOGOUT
def logout_view(request):
    return redirect("home")


#-----------------------------------------------------------

#ARBEITSBERICHTE-BEREICH

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


def arbeitsberichte_view(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break

    if not user:
        return redirect("login")
    
    berichte = lade_berichte()
    #neuen bericht speichern
    if request.method == "POST":
        modul = request.POST.get("modul")
        datum = request.POST.get("datum")
        minuten = int(request.POST.get("minuten"))
        inhalt = request.POST.get("inhalt")

        if minuten and modul and inhalt is not None:
            try:
                minuten = int(minuten)
            except ValueError:
                minuten = 0

            neuer_bericht = Arbeitsberichte(
                username=user.username,
                modul=modul,
                datum=datum,
                minuten=minuten,
                inhalt=inhalt
            )
            
            berichte.insert(0, neuer_bericht.to_dict())
            speichere_berichte(berichte)

        return redirect(f"/arbeitsberichte?user_id={user.id}")

    #nur eigenen berichte angezeigt
    eigene_berichte = []
    for b in berichte:
        if b["username"] == user.username:
            eigene_berichte.append(b)
    
    #module laden
    modules = load_modules()

    return render(request, "meine_app/arbeitsberichte.html", {
        "arbeitsberichte": eigene_berichte,
        "role": user.role,
        "user": user,
        "modules": modules,
        "user_id": user.id,
        })


def bericht_loeschen(request, index):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if not user:
        return redirect("login")
    
    berichte = lade_berichte()

    neue_liste = []
    aktueller_index = 0

    for b in berichte:
        if aktueller_index == index and b["username"] == user.username:
            pass
        else:
            neue_liste.append(b)
        
        aktueller_index += 1
    
    speichere_berichte(neue_liste)
    
    return redirect(f"/arbeitsberichte?user_id={user.id}")


#-----------------------------------------------------------

#GESAMTÜBERSICHT
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


#GESAMTÜBERSICHT
def gesamtuebersicht(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()

    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break

    if user is None:
        return redirect("login")

    daten = prozentanteile(user.username)
    return render(request, "meine_app/gesamtuebersicht.html", {
        "daten": daten,
        "user": user,
        "user_id": user.id
    })


#-----------------------------------------------------------

#ADMIN-BEREICH

#admin: MODULE FESTLEGEN
def load_modules():
    try:
        with open(pfad_modules, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("modules", [])
    except FileNotFoundError:
        return []

def save_modules(modules_list):
    data = {"modules": modules_list}
    with open(pfad_modules, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def admin_modules(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()

    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if user is None:
        return redirect("login")
    
    if user.role != "admin":
        return HttpResponse("Zugriff verweigert - keine Admin-Rechte.")
    

    if request.method == "POST":
        text = request.POST.get("module")

        if not text:
            return redirect(f"/admin_modules?user_id={user.id}")
        
        modules_list = []
        for m in text.split("\n"):
            m = m.strip()
            if m:
                modules_list.append(m)

        save_modules(modules_list)
        return redirect(f"/arbeitsberichte?user_id={user.id}")
    

    modules = load_modules()
    modules_text = ""
    for m in modules:
        modules_text += m + "\n"

    return render(request, "meine_app/admin_modules.html", {
        "modules_text": modules_text,
        "user": user,
        "user_id": user.id
    })


#----------------------------------------------------------

#VIP ANFRAGEN
def request_vip(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if user is None:
        return redirect("login")
    
    if user.role != "einfach":
        return redirect(f"/arbeitsberichte?user_id={user.id}")

    user.vip_request = True
    save_users(users)

    return redirect(f"/arbeitsberichte?user_id={user.id}")

#einf. anw. bestätigt anfrage:
def bestaetige_vip(request):
    user_id = request.GET.get("user_id")
    return render(request, "meine_app/bestaetige_vip.html", {
        "user_id": user_id
    })


#ADMIN ANFRAGEN
def request_admin(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break

    if user is None:
        return redirect("login")

    if user.role != "vip":
        return redirect(f"/arbeitsberichte?user_id={user.id}")
    
    user.admin_request = True
    save_users(users)
    
    return redirect(f"/arbeitsberichte?user_id={user.id}")

#vip bestätigt anfrage:
def bestaetige_admin(request):
    user_id = request.GET.get("user_id")
    return render(request, "meine_app/bestaetige_admin.html", {
        "user_id": user_id
    })


#-------------------------------------------
#ADMIN: LISTE ALLER ANFRAGEN + GENEHMIGUNGEN
def admin_request_list(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()

    #benutzer anhand id finden
    aktueller_user = None
    for u in users:
        if str(u.id) == user_id:
            aktueller_user = u
            break

    if aktueller_user is None:
        return redirect("login")
    
    #prüfen ob admin
    if aktueller_user.role != "admin":
        return redirect(f"/arbeitsberichte?user_id={aktueller_user.id}")
    
    #alle offenen anträge
    offene = []
    for u in users:
        if u.vip_request or u.admin_request:
            offene.append(u)

    return render(request, "meine_app/admin_request_list.html", {
        "requests": offene,
        "user": aktueller_user,
        "user_id": aktueller_user.id
    })


def genehmige_vip(request, email):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()

    aktueller_user = None
    for u in users:
        if str(u.id) == user_id:
            aktueller_user = u
            break
    users = load_users()

    if aktueller_user is None or aktueller_user.role != "admin":
        return redirect("login")
    
    for u in users:
        if u.email == email:
            u.role = "vip"
            u.vip_request = False
            break
    
    save_users(users)
    return redirect(f"/admin/request-list?user_id={aktueller_user.id}")

def genehmige_admin(request, email):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()

    aktueller_user = None
    for u in users:
        if str(u.id) == user_id:
            aktueller_user = u
            break
    
    if aktueller_user is None or aktueller_user.role != "admin":
        return redirect("login")
    
    for u in users:
        if u.email == email:
            u.role = "admin"
            u.admin_request = False
            break

    save_users(users)

    return redirect(f"/admin/request-list?user_id={aktueller_user.id}")


#------------------------------
def admin_user_list(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()

    aktueller_user = None
    for u in users:
        if str(u.id) == user_id:
            aktueller_user = u
            break
    
    if aktueller_user is None or aktueller_user.role != "admin":
        return redirect("login")
    
    return render(request, "meine_app/admin_user_list.html", {
        "users": users,
        "user": aktueller_user,
        "user_id": aktueller_user.id
    })


#admin: USER SPERREN
def user_sperren(request, target_id):
    admin_id = request.GET.get("user_id")
    if not admin_id:
        return redirect("login")

    users = load_users()

    aktueller_user = None
    for u in users:
        if str(u.id) == admin_id:
            aktueller_user = u
            break
    
    if aktueller_user is None or aktueller_user.role != "admin":
        return redirect("login")

    for u in users:
        if u.id == target_id:
            u.is_active = False
            break
    
    save_users(users)

    return redirect(f"/admin/user-list?user_id={aktueller_user.id}")

#admin: USER ENTSPERREN
def user_entsperren(request, target_id):
    admin_id = request.GET.get("user_id")
    if not admin_id:
        return redirect("login")

    users = load_users()

    aktueller_user = None
    for u in users:
        if str(u.id) == admin_id:
            aktueller_user = u
            break
    
    if aktueller_user is None or aktueller_user.role != "admin":
        return redirect("login")
    
    for u in users:
        if u.id == target_id:
            u.is_active = True
            break
    
    save_users(users)

    return redirect(f"/admin/user-list?user_id={aktueller_user.id}")


#----------------------------------------------------------
#VIP-BEREICH

#DOWNLOADS
def download_json(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if user is None:
        return redirect("login")
    
    berichte = lade_berichte()

    eigene = []
    for b in berichte:
        if b["username"] == user.username:
            eigene.append(b)
    
    text = json.dumps(eigene, indent=4, ensure_ascii=False)

    response = HttpResponse(text, content_type="application(json")
    response["Content-Disposition"] = 'attachment; filename="berichte.json"'
    return response

def download_csv(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if user is None:
        return redirect("login")
    
    berichte = lade_berichte()

    eigene = []
    for b in berichte:
        if b["username"] == user.username:
            eigene.append(b)
    
    text = "modul,datum,minuten,inhalt\n"
    for b in eigene:
        text += f"{b['modul']}, {b['datum']}, {b['minuten']}, {b['inhalt']}\n"

    response = HttpResponse(text, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="berichte.csv"'
    return response

def download_xml(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if user is None:
        return redirect("login")
    
    berichte = lade_berichte()

    eigene = []
    for b in berichte:
        if b["username"] == user.username:
            eigene.append(b)
    
    text = "<arbeitsberichte>\n"

    for b in eigene:
        text += "  <bericht>\n"
        text += f"    <modul>{b['modul']}</modul>\n"
        text += f"    <datum>{b['datum']}</datum>\n"
        text += f"    <minuten>{b['minuten']}</minuten>\n"
        text += f"    <inhalt>{b['inhalt']}</inhalt>\n"
        text += "  </bericht>\n"

    text += "</arbeitsberichte>"

    response = HttpResponse(text, content_type="application/xml")
    response["Content-Disposition"] = 'attachment; filename="berichte.xml"'
    return response

#-------
#UPLOAD 
def upload_data(request):
    if request.method != "POST":
        return redirect("arbeitsberichte")
    
    user_id = request.GET.get("user_id")
    if not user_id:
        return redirect("login")
    
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    
    if user is None:
        return redirect("login")

    datei = request.FILES.get("datei")
    if not datei:
        return redirect(f"/arbeitsberichte?user_id={user.id}")
    
    alle = lade_berichte()
    neue = []

    #JSON
    if datei.name.endswith(".json"):
        neue = json.load(datei)
        for b in neue:
            b["username"] = user.username
    
    else:
        return redirect(f"/arbeitsberichte?user_id={user.id}")
    
    neue_liste = []
    for b in alle:
        if b["username"] != user.username:
            neue_liste.append(b)
    
    for b in neue:
        neue_liste.append(b)

    speichere_berichte(neue_liste)

    return redirect(f"/arbeitsberichte?user_id={user.id}")

