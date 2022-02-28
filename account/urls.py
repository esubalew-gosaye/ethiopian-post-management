from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('', views.login, name="login"),
    path('register<str:role>/', views.register, name="register"),
    path('tempo/', views.tempo, name="tempo-view"),
    path('update_password/<str:pk>/', views.update_password, name='update_password'),
    path('logout/', views.logout, name="logout")
]