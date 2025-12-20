from django.shortcuts import render, redirect
from .models import UserData, load_users, save_users
from .models import Arbeitsberichte, lade_berichte, speichere_berichte

import json
from pathlib import Path
from django.http import JsonResponse

def home(request):
    return render(request, "meine_app/home.html")

#registrierung
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

        return redirect("success")
    
    return render(request, "meine_app/register.html")

def success(request):
    return render(request, "meine_app/success.html")


#arbeitsberichte
def arbeitsberichte_view(request):
    berichte = lade_berichte()

    if request.method == "POST":
        modul = request.POST.get("modul")
        datum = request.POST.get("datum")
        min = request.POST.get("min")
        inhalt = request.POST.get("inhalt")

        if min and modul and inhalt:
            neuer_bericht = Arbeitsberichte(modul, datum, min, inhalt)
            berichte.insert(0, neuer_bericht.to_dict())
            speichere_berichte(berichte)
        return redirect("arbeitsberichte")

    return render(request, "meine_app/arbeitsberichte.html", {"arbeitsberichte": berichte})


'''
#Aufg. json &/ csv Datenquelle online stellen & link teilen
def online_datenquelle(request):

    BASE_DIR = Path(__file__).resolve().parent
    json_path = BASE_DIR / "data" / "userdata.json"

    with open(json_path, "r") as f:
        data = json.load(f)

    return JsonResponse({"users": data})
'''