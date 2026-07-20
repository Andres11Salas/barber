from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'password', 'telefono', 'bio', 'rol', 'estado', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'password': {'write_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'telefono', 'bio', 'rol']
        read_only_fields = ['id', 'email', 'rol']


class ActualizarPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'telefono', 'bio']
