from django.urls import path
from meine_app import views as app_views
from django.contrib.auth import views as auth_views #vorgefertigte Views für Benutzer-Authentifizierung
from django.views.generic import TemplateView

urlpatterns = [
    path('anmelden/', auth_views.LoginView.as_view(template_name='meine_app/login.html'), name='userauth_login'),
    path('abmelden/', auth_views.LogoutView.as_view(next_page='/'), name='userauth_logout'),
    path('passwort-aendern/', auth_views.PasswordChangeView.as_view(template_name='meine_app/password_change_form.html'), name='userauth_password_change'),
    path('passwort-geaendert/', auth_views.PasswordChangeDoneView.as_view(template_name='meine_app/password_change_done.html'), name='userauth_password_change_done'),
    path('registrieren/', app_views.register, name='userauth_register'),
    path('willkommen/', TemplateView.as_view(template_name='meine_app/register_done.html'), name='userauth_register_done'),

    #path("", app_views.servus),
    #path("wiespät", app_views.jetzt),
]
