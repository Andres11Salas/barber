import random
import string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from apps.usuarios.models import Usuario
from .serializers import (
    LoginSerializer, RegistroSerializer,
    RecuperarPasswordSerializer
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
