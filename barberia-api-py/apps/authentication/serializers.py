import random
import string
from rest_framework import serializers
from apps.usuarios.models import Usuario


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RegistroSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este correo ya está registrado.')
        return value


class RecuperarPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('No existe una cuenta con este correo.')
        return value


class AuthResponseSerializer(serializers.Serializer):
    mensaje = serializers.CharField()
    token = serializers.CharField(required=False)
    rol = serializers.CharField(required=False)


class GoogleRegisterSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    nombre = serializers.CharField(required=False, allow_blank=True)
