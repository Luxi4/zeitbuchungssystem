from django.shortcuts import render, redirect
from .models import UserData, load_users, save_users

def home(request):
    return render(request, "meine_app/home.html")

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
