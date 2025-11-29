from django.shortcuts import render, redirect
from .models import UserData, load_users, save_users

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
pfad_arbeitsberichte = BASE_DIR / "data" / "arbeitsberichte.json"

def arbeitsberichte(request):
    # arbeitsberichte laden
    try:
        with open(pfad, 'r') as f:
            arbeitsberichte = json.load(f)
    except Exception:
        arbeitsberichte = []

    if request.method == "POST":
        name = request.COOKIES.get('nutzername')  # Benutzername aus Cookies holen

        # Nicht eingeloggt
        if not name:
            return render(request, 'accounts/event_angeklickt.html', {
                'arbeitsberichte': arbeitsberichte,
                'fehler': "Du musst eingeloggt sein, um zu kommentieren oder zu liken."
            })

        # Kommentar wurde abgeschickt - neuer Kommentar an Liste anhängen
        text = request.POST.get('text')
        if text:
            zeit = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M")
            arbeitsberichte.append({
                "name": name,
                "zeit": zeit,
                "text": text,
                "likes": 0,
                "geliket_von": []
            })

            with open(pfad, 'w') as f:
                json.dump(arbeitsberichte, f)

            return redirect('home')

    return render(request, 'arbeitsberichte.html', {
        'arbeitsberichte': arbeitsberichte,
        'username': request.COOKIES.get('username')
    })