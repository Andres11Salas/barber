import random
import string
import requests as http_requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from apps.usuarios.models import Usuario
from .serializers import (
    LoginSerializer, RegistroSerializer,
    RecuperarPasswordSerializer, GoogleRegisterSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        usuario = Usuario.objects.get(email=serializer.validated_data['email'])
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if usuario.password != serializer.validated_data['password']:
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

    token = AccessToken.for_user(usuario)
    token['rol'] = usuario.rol

    return Response({
        'mensaje': f'Bienvenido {usuario.nombre}',
        'token': str(token),
        'rol': usuario.rol,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    serializer = RegistroSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    usuario = Usuario.objects.create(
        nombre=serializer.validated_data['nombre'],
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        rol='CLIENTE',
    )

    return Response(
        {'mensaje': '¡Cuenta creada con éxito! Ya puedes iniciar sesión.'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def recuperar(request):
    serializer = RecuperarPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    usuario = Usuario.objects.get(email=serializer.validated_data['email'])
    password_temporal = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    usuario.password = password_temporal
    usuario.save()

    return Response({
        'mensaje': 'Se ha restablecido tu acceso.',
        'instruccion': f'Tu contraseña temporal es: {password_temporal}. Inicia sesión y cámbiala.',
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def google_register(request):
    serializer = GoogleRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    id_token = serializer.validated_data['id_token']

    try:
        resp = http_requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}',
            timeout=10
        )
        if resp.status_code != 200:
            raise Exception('Token inválido')
        info = resp.json()
        if info.get('aud') != settings.GOOGLE_CLIENT_ID:
            return Response(
                {'error': 'El token no pertenece a esta aplicación.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception:
        return Response(
            {'error': 'El token de Google no es válido o ha expirado.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    email = info.get('email')
    nombre = serializer.validated_data.get('nombre') or info.get('name', 'Usuario Google')

    if not email:
        return Response(
            {'error': 'No se pudo obtener el correo de tu cuenta de Google.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    usuario, created = Usuario.objects.get_or_create(
        email=email,
        defaults={
            'nombre': nombre,
            'password': f'google_{random.choices(string.ascii_letters + string.digits, k=16)}',
            'rol': 'CLIENTE',
        }
    )

    if created:
        mensaje = 'Cuenta creada con Google. ¡Bienvenido!'
    else:
        mensaje = 'Inicio de sesión con Google exitoso. Bienvenido de nuevo.'

    token = AccessToken.for_user(usuario)
    token['rol'] = usuario.rol

    return Response({
        'mensaje': mensaje,
        'token': str(token),
        'rol': usuario.rol,
        'nombre': usuario.nombre,
    })
