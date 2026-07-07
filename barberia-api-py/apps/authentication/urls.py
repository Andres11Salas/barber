from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='auth-login'),
    path('registro', views.registro, name='auth-registro'),
    path('recuperar', views.recuperar, name='auth-recuperar'),
]
