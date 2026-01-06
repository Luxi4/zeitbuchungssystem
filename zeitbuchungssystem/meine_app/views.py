from django.shortcuts import render, redirect
from .models import UserData, load_users, save_users
from .models import Arbeitsberichte, lade_berichte, speichere_berichte
from .models import zeit_pro_modul, pfad_arbeitsberichte, prozentanteile
from django.http import HttpResponse
import json

from pathlib import Path
from django.http import JsonResponse

def home(request):
    return render(request, "meine_app/home.html")

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

        new_user = UserData(username, email, password, role="einfach")
        users.append(new_user)
        save_users(users)

        #benutzer nach registrierung automatisch einloggen
        request.session["username"] = username
        request.session["user_email"] = email

        return redirect("arbeitsberichte")
    
    return render(request, "meine_app/register.html")

def success(request):
    return render(request, "meine_app/success.html")

#LOGIN
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        users = load_users()

        for u in users:
            if u.email == email and u.password == password:
                request.session["user_email"] = u.email
                request.session["username"] = u.username
        
                return redirect("arbeitsberichte")
        
        return render(request, "meine_app/login.html", {"error": "Login fehlgeschlagen!"})
    
    return render(request, "meine_app/login.html")

#LOGOUT
def logout_view(request):
    request.session.flush() #löscht alle session-daten
    return redirect("home")



#ARBEITSBERICHTE
def arbeitsberichte_view(request):
    email = request.session.get("user_email")
    users = load_users()

    #zuerst user finden
    user = None
    for u in users:
        if u.email == email:
            user = u
            break

    if user is None:
        return redirect("login")

    
    berichte = lade_berichte()

    if request.method == "POST":
        modul = request.POST.get("modul")
        datum = request.POST.get("datum")
        minuten = int(request.POST.get("minuten"))
        inhalt = request.POST.get("inhalt")

        if minuten and modul and inhalt is not None:
            username = request.session.get("username")

            neuer_bericht = Arbeitsberichte(username=username, modul=modul, datum=datum, minuten=minuten, inhalt=inhalt)
            
            berichte.insert(0, neuer_bericht.to_dict())
            speichere_berichte(berichte)

        return redirect("arbeitsberichte")

    username = request.session.get("username")
    eigene_berichte = []
    for b in berichte:
        if b["username"] == username:
            eigene_berichte.append(b)
    
    return render(request, "meine_app/arbeitsberichte.html", {
        "arbeitsberichte": eigene_berichte,
        "role": user.role,
        "user": user
        })



#VIP ANFRAGEN
def request_vip(request):
    email = request.session.get("user_email")
    users = load_users()

    for u in users:
        if u.email == email:
            if u.role != "einfach":
                return redirect("arbeitsberichte")
            u.vip_request = True
            break
    
    save_users(users)
    return redirect("arbeitsberichte")

#einf. anw. bestätigt anfrage:
def bestätige_vip(request):
    return render(request, "meine_app/bestätige_vip.html")

#ADMIN ANFRAGEN
def request_admin(request):
    email = request.session.get("user_email")
    users = load_users()

    for u in users:
        if u.email == email:
            if u.role != "vip":
                return redirect("arbeitsberichte")
            u.admin_request = True
            break
    
    save_users(users)
    return redirect("arbeitsberichte")

#vip bestätigt anfrage:
def bestätige_admin(request):
    return render(request, "meine_app/bestätige_admin.html")


#ADMIN: liste aller anfragen
def admin_request_list(request):
    email = request.session.get("user_email")
    users = load_users()

    #1. aktuellen user
    aktueller_user = None
    for u in users:
        if u.email == email:
            aktueller_user = u
            break
    #2. prüfen ob admin
    if aktueller_user is None or aktueller_user.role != "admin":
        return redirect("arbeitsberichte")
    #3. alle offenen anträge
    offene = []
    for u in users:
        if u.vip_request or u.admin_request:
            offene.append(u)

    return render(request, "meine_app/admin_request_list.html", {
        "requests": offene
    })

def genehmige_vip(request, email):
    users = load_users()

    for u in users:
        if u.email == email:
            u.role = "vip"
            u.vip_request = False
            break
    
    save_users(users)
    return redirect("admin_request_list")

def genehmige_admin(request, email):
    users = load_users()

    for u in users:
        if u.email == email:
            u.role = "admin"
            u.admin_request = False
            break
    
    save_users(users)
    return redirect("admin_request_list")


def admin_user_list(request):
    users = load_users()
    return render(request, "meine_app/admin_user_list.html", {"users": users})



#GESAMTÜBERSICHT
def gesamtübersicht(request):
    username = request.session["username"]
    if not username:
        return redirect("login")
    daten = prozentanteile(username)
    return render(request, "meine_app/gesamtübersicht.html", {"daten": daten})



#DOWNLOADS



'''
#Aufg. json &/ csv Datenquelle online stellen & link teilen
def online_datenquelle(request):

    BASE_DIR = Path(__file__).resolve().parent
    json_path = BASE_DIR / "data" / "userdata.json"

    with open(json_path, "r") as f:
        data = json.load(f)

    return JsonResponse({"users": data})
'''