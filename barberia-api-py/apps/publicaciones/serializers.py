from rest_framework import serializers
from .models import Publicacion, Comentario, Reaccion
from apps.usuarios.serializers import UsuarioPerfilSerializer


class UsuarioMinSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()


class ComentarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioPerfilSerializer(read_only=True)
    usuario_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'publicacion_id', 'usuario', 'usuario_id', 'texto', 'createdAt']
        extra_kwargs = {
            'createdAt': {'read_only': True},
        }


class ReaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaccion
        fields = ['id', 'publicacion_id', 'usuario_id', 'tipo', 'createdAt']
        extra_kwargs = {
            'createdAt': {'read_only': True},
            'usuario_id': {'read_only': True},
        }


class PublicacionSerializer(serializers.ModelSerializer):
    barbero = UsuarioPerfilSerializer(read_only=True)
    barbero_id = serializers.IntegerField(write_only=True)
    comentarios = ComentarioSerializer(many=True, read_only=True)
    reacciones = ReaccionSerializer(many=True, read_only=True)

    class Meta:
        model = Publicacion
        fields = ['id', 'barbero', 'barbero_id', 'titulo', 'descripcion',
                  'contenido_json', 'likes_count', 'dislikes_count',
                  'comentarios', 'reacciones', 'createdAt']
        extra_kwargs = {
            'createdAt': {'read_only': True},
            'likes_count': {'read_only': True},
            'dislikes_count': {'read_only': True},
        }


class ComentarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['texto']


class ReaccionCreateSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=['like', 'dislike'])
