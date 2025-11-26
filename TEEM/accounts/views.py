import uuid
import re
import json
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
import os
import datetime
from django.views.generic.edit import CreateView
from .models import Address
#from .models import Event
# from .models import Kommentar


#Kommentare
pfad = os.path.join(settings.BASE_DIR, 'kommentare.json') #BASE_DIR = Hauptordner v. Projekt (wo auch manage.py/django-projekt)

def event_angeklickt(request):
    # Kommentare laden
    try:
        with open(pfad, 'r') as f:
            kommentare = json.load(f)
    except Exception:
        kommentare = []

    if request.method == "POST":
        name = request.COOKIES.get('nutzername')  # Benutzername aus Cookies holen

        # Nicht eingeloggt
        if not name:
            return render(request, 'accounts/event_angeklickt.html', {
                'kommentare': kommentare,
                'fehler': "Du musst eingeloggt sein, um zu kommentieren oder zu liken."
            })

        # Like-Button wurde gedrückt
        like_index = request.POST.get('like') #aus abgeschickten Formular (POST-Daten) wird Wert des Feldes "like" geholt
        if like_index is not None and like_index.isdigit(): #isdigit prüft ob Zahlen sind
            index = int(like_index) #(index = Position des Kommentars in Liste)
            if 0 <= index < len(kommentare): #prüft ob Zahl index zw. 0 und Kommentaranzahl
                if name in kommentare[index]['geliket_von']: #wenn name in Liste geliket_von
                    kommentare[index]['likes'] -= 1
                    kommentare[index]['geliket_von'].remove(name)
                else:
                    kommentare[index]['likes'] += 1
                    kommentare[index]['geliket_von'].append(name)

                with open(pfad, 'w') as f:
                    json.dump(kommentare, f)

                # Nach Like sofort weiterleiten, damit Reload funktioniert
                return redirect('home')

        # Kommentar wurde abgeschickt - neuer Kommentar an Liste anhängen
        text = request.POST.get('text')
        if text:
            zeit = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M")
            kommentare.append({
                "name": name,
                "zeit": zeit,
                "text": text,
                "likes": 0,
                "geliket_von": []
            })

            with open(pfad, 'w') as f:
                json.dump(kommentare, f)

            return redirect('home')

    return render(request, 'event_angeklickt.html', {
        'kommentare': kommentare,
        'nutzername': request.COOKIES.get('nutzername')
    })


# Speicherort der JSON-Datei
PFAD = Path(__file__).resolve().parent.parent / "user_data.json"

def check_login(request):
    """Prüft, ob der Nutzer eingeloggt ist (per Cookie)."""
    return bool(request.COOKIES.get("nutzername"))

def nutzer_ausgeben(request):
    """Gibt den aktuellen Nutzer aus user_data.json zurück oder None."""
    nutzername = request.COOKIES.get("nutzername")
    if not nutzername:
        return None
    
    nutzer_liste = lade_nutzer()
    for nutzer in nutzer_liste:
        if nutzer["nutzername"] == nutzername:
            return nutzer  # Gibt das gesamte Nutzer-Dict zurück
    return None

def lade_nutzer():
    if not PFAD.exists():
        return []
    with open(PFAD, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_nutzer(nutzer):
    daten = lade_nutzer()
    daten.append(nutzer)
    with open(PFAD, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2)

def aktualisiere_nutzer(code):
    daten = lade_nutzer()
    for nutzer in daten:
        if nutzer["code"] == code and not nutzer["bestaetigt"]:
            nutzer["bestaetigt"] = True
            with open(PFAD, "w", encoding="utf-8") as f:
                json.dump(daten, f, indent=2)
            return nutzer
    return None

def registrieren(request):
    if request.method == "POST":
        nutzername = request.POST["nutzername"]
        email = request.POST["email"]
        passwort = request.POST["passwort"]

        code = uuid.uuid4().hex
        nutzer = {
            "nutzername": nutzername,
            "email": email,
            "passwort": passwort,  # In Produktion nie im Klartext speichern!
            "code": code,
            "bestaetigt": False
        }

        speichere_nutzer(nutzer)

        bestätigungslink = request.build_absolute_uri(
            reverse("bestaetigen", kwargs={"code": code})
        )

        # Text-Version der E-Mail (send_mail sendet standardmäßig nur Plaintext)
        nachricht = (
            f"Hallo {nutzername},\n\n"
            f"Bitte bestätige dein Konto, indem du auf diesen Link klickst: {bestätigungslink}\n\n"
            "Viele Grüße,\n"
            "Dein Team"
        )


        send_mail(
            subject="Bitte bestätige deine E-Mail-Adresse",
            message=nachricht,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return render(request, "konto_erstellt.html", {"nutzer": nutzer})

    return render(request, "registrieren.html")

def bestaetigen(request, code):
    nutzer = aktualisiere_nutzer(code)
    if nutzer:
        return render(request, "bestaetigt.html", {"nutzer": nutzer})
    else:
        return render(request, "ungültiger_code.html")
    
def einloggen(request):
    if request.method == "POST":
        email = request.POST.get("email")
        passwort = request.POST.get("passwort")

        nutzer_liste = lade_nutzer()
        for nutzer in nutzer_liste:
            if nutzer["email"] == email and nutzer["passwort"] == passwort:
                if not nutzer["bestaetigt"]:
                    hinweis = "Bitte bestätige zuerst deine E-Mail-Adresse."
                    return render(request, "login.html", {"hinweis": hinweis})

                # Login erfolgreich – Cookie setzen
                response = redirect("konto")
                response.set_cookie("nutzername", nutzer["nutzername"], max_age=86400)  # 1 Tag
                return response

        hinweis = "Ungültige Anmeldedaten."
        return render(request, "login.html", {"hinweis": hinweis})

    return render(request, "login.html")

def konto(request):
    nutzername = request.COOKIES.get("nutzername")
    if not nutzername:
        return redirect("login")
    return render(request, "konto.html", {"nutzername": nutzername})

def logout(request):
    response = redirect("login")
    response.delete_cookie("nutzername")
    return response

def my_account(request):
    if not check_login(request):
        return redirect("login")
    
    nutzer = nutzer_ausgeben(request)
    if not nutzer:
        messages.error(request, "Benutzer nicht gefunden!")
        return redirect("login")
    
    return render(request, "myAccount.html", {
        "nutzername": nutzer["nutzername"],
        "email": nutzer["email"]
    })
'''
def my_events(request):
    if not check_login(request):
        return redirect("login")
    return render(request, "myEvents.html")
    '''

def about(request):
    return render(request, "about.html")


# Create your views here.
class AddressView(CreateView):
    model = Address
    fields = ['title', 'date', 'address', 'description'] # Felder die eingetragen werden von models; evtl hier & bei models dann noch Beschreibung dazu?
    template_name = 'myEvents.html'
    success_url = '/myevents' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = 'pk.eyJ1IjoidGVlbTEiLCJhIjoiY21jOW00eWgyMDQ1cjJzc2x2NnloZDI4MiJ9.RsKX8bG-FaDg7loiIJ5wgg'
        context['addresses'] = Address.objects.all()
        return context 
    
