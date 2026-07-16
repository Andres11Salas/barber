from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^crear$', views.crear_preferencia_pago, name='crear-pago'),
    re_path(r'^webhook$', views.recibir_webhook, name='webhook-pago'),
]