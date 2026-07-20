from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login', views.login, name='auth-login'),
    path('registro', views.registro, name='auth-registro'),
    path('recuperar', views.recuperar, name='auth-recuperar'),
    path('google', views.google_register, name='auth-google'),
    path('refresh', TokenRefreshView.as_view(), name='auth-refresh'),
]
