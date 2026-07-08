from rest_framework import serializers
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


class CrearPreferenciaSerializer(serializers.Serializer):
    citaId = serializers.IntegerField()
    monto = serializers.DecimalField(max_digits=10, decimal_places=2)
    descripcion = serializers.CharField(required=False, default='Corte de Cabello / Servicio de Barbería')