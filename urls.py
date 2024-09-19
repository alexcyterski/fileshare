from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:dir>", views.index, name="index"),
    path('download/<str:dir>/<str:file_name>', views.download, name="download"),
    path('delete/<str:dir>/<str:file_name>', views.delete, name="delete")
]