from django.urls import path
from meine_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("success/", views.success, name="success"),
    path("arbeitsberichte/", views.arbeitsberichte_view, name="arbeitsberichte"),
    path("gesamtuebersicht/", views.gesamtuebersicht, name="gesamtuebersicht"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path("bestaetige_vip/", views.bestaetige_vip, name="bestaetige_vip"),
    path("request_vip/", views.request_vip, name="request_vip"),
    path("genehmige/vip/<str:email>/", views.genehmige_vip, name="genehmige_vip"),
    path("bestaetige_admin/", views.bestaetige_admin, name="bestaetige_admin"),
    path("request_admin/", views.request_admin, name="request_admin"),
    path("genehmige/admin/<str:email>/", views.genehmige_admin, name="genehmige_admin"),
    path("admin/request-list/", views.admin_request_list, name="admin_request_list"),
    path("admin/user-list", views.admin_user_list, name="admin_user_list"),
    path('admin/user/<int:user_id>/sperren/', views.user_sperren, name='user_sperren'),
    path('admin/user/<int:user_id>/entsperren/', views.user_entsperren, name='user_entsperren'),
    path("admin_modules/", views.admin_modules, name="admin_modules"),
    
    path("download/json/", views.download_json, name="download_json"),
    path("download/csv/", views.download_csv, name="download_csv"),
    path("download/xml/", views.download_xml, name="download_xml"),
    path("upload/", views.upload_data, name="upload_data"),

]
