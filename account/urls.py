from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('', views.login, name="login"),
    path('register<str:role>/', views.register, name="register"),
    path('delete/<str:pk>/', views.delete_user, name="delete-user"),
    path('update_password/<str:pk>/', views.update_password, name='update_password'),
    path('update_password_forgot/<str:pk>/', views.update_password_forgot, name='update_password_forgot'),
    path('update_account/', views.update_account, name='update_account'),
    path('forgot_password/', views.forgot_password, name="revoke-new-password"),
    path('logout/', views.logout, name="logout")
]