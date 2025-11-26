from django.urls import path
from meine_app import views as app_views

urlpatterns = [
    path("", app_views.setcookie),
    path("wiespät", app_views.jetzt),
]
