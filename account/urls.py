# Django 
from django.urls import path
from django.contrib.auth import views as auth_views
# Apps de Dawipo
from . import views

# Urls de la app de usuarios y cuentas.
urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'), 
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'), 
    path('edit/', views.edit, name='edit'), 
]