from django.urls import path
from meine_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("success/", views.success, name="success"),
    path("arbeitsberichte/", views.arbeitsberichte_view, name="arbeitsberichte"),
    path("gesamtübersicht/", views.gesamtübersicht, name="gesamtübersicht"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("bestätige_vip/", views.bestätige_vip, name="bestätige_vip"),
    path("request_vip/", views.request_vip, name="request_vip"),
    path("admin/vip/genehmige/<str:email>/", views.genehmige_vip, name="genehmige_vip"),
    path("admin/vip-list/", views.admin_vip_list, name="admin_vip_list"),
    path("admin/user-list", views.admin_user_list, name="admin_user_list"),

    #path("datenquelle/", views.online_datenquelle),
]
