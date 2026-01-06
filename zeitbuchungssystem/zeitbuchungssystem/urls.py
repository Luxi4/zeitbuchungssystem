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
    path("genehmige/admin/<str:email>/", views.genehmige_admin, name="genehmige_admin"),
    path("admin/request-list/", views.admin_request_list, name="admin_request_list"),
    path("admin/user-list", views.admin_user_list, name="admin_user_list"),
    path("request_admin/", views.request_admin, name="request_admin"),

    path("download/json/", views.download_json, name="download_json"),
    path("download/csv/", views.download_csv, name="download_csv"),
    path("download/xml/", views.download_xml, name="download_xml"),
    path("upload/", views.upload_data, name="upload_data"),


    #path("datenquelle/", views.online_datenquelle),
]
