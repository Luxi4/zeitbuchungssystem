from django.urls import path
from .views import AddressView
from . import views

urlpatterns = [ #Pfade die inputs + map anzeigen sollen brauchen AddressView und nicht views.xy !!
    path('registrierung/', views.registrieren, name='registrieren'),
    path('', views.registrieren, name='registrieren'),
    path('bestaetigen/<str:code>/', views.bestaetigen, name='bestaetigen'),
    path('login/', views.einloggen, name='login'),  # ← hinzugefügt
    path('konto/', views.konto, name='konto'),      # ← Beispielziel nach Login
    path('logout/', views.logout, name='logout'),
    path("home/", views.event_angeklickt, name="home"),
    path("myaccount/", views.my_account, name="my_account"),
    path("myevents/", AddressView.as_view(), name="my_events"),
    path("about/", views.about, name="about"),
]
