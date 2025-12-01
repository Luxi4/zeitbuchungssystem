from django.urls import path
from meine_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("success/", views.success, name="success"),
    #path("arbeitsberichte/", views.arbeitsberichte, name="arbeitsberichte"),
    path("datenquelle/", views.online_datenquelle),
]
