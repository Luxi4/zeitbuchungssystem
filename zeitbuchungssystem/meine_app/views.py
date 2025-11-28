from django.shortcuts import render, redirect
from .models import UserData, load_users, save_users

def home(request):
    return render(request, "meine_app/home.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "einfach")

        users = load_users()

        #Prüfen, ob E-Mail schon existiert
        if any(u.email == email for u in users):
            return render(request, "register.html", {"error": "E-Mail bereits registriert!"})

        new_user = UserData(username, email, password, role)
        users.append(new_user)
        save_users(users)

        return redirect("success")
    
    return render(request, "meine_app/register.html")

def success(request):
    return render(request, "meine_app/success.html")
