from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.usuarios.models import Usuario


class UsuarioJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado', code='user_not_found')
