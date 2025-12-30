from django.urls import path
from meine_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("success/", views.success, name="success"),
    path("arbeitsberichte/", views.arbeitsberichte_view, name="arbeitsberichte"),
    #path("gesamtübersicht/", views.gesamtübersicht, name="gesamtübersicht"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("logout-success/", views.logout_success, name="logout_success"),

    #path("datenquelle/", views.online_datenquelle),
]
