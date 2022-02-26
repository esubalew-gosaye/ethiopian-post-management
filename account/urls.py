from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('', views.index, name="index"),
    path('register<str:role>/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="log-out"),
    path('admin-dashboard/', views.admin, name="admin-dashboard"),
]