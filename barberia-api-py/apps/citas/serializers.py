from rest_framework import serializers
from .models import Cita
from apps.usuarios.serializers import UsuarioPerfilSerializer
from apps.servicios.serializers import ServicioSerializer


class CitaSerializer(serializers.ModelSerializer):
    cliente = UsuarioPerfilSerializer(read_only=True)
    barbero = UsuarioPerfilSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)
    cliente_id = serializers.IntegerField(write_only=True)
    barbero_id = serializers.IntegerField(write_only=True)
    servicio_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cita
        fields = ['id', 'cliente', 'barbero', 'servicio', 'cliente_id', 'barbero_id',
                  'servicio_id', 'fecha', 'hora', 'estado', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
            'estado': {'read_only': True},
        }
