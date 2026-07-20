from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Q
from .models import Publicacion, Comentario, Reaccion
from .serializers import (
    PublicacionSerializer, ComentarioSerializer,
    ComentarioCreateSerializer, ReaccionCreateSerializer
)
from apps.usuarios.permissions import EsBarberoOAdmin


class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.select_related('barbero').prefetch_related(
        'comentarios__usuario', 'reacciones'
    ).all()
    serializer_class = PublicacionSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), EsBarberoOAdmin()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(barbero_id=self.request.user.id)

    @action(detail=False, methods=['get'], url_path='barbero/(?P<barbero_id>[^/.]+)')
    def por_barbero(self, request, barbero_id=None):
        publicaciones = self.queryset.filter(barbero_id=barbero_id)
        serializer = self.get_serializer(publicaciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated()])
    def reacciones(self, request, pk=None):
        publicacion = self.get_object()
        serializer = ReaccionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo = serializer.validated_data['tipo']

        reaccion, created = Reaccion.objects.get_or_create(
            publicacion=publicacion,
            usuario_id=request.user.id,
            defaults={'tipo': tipo}
        )

        if not created:
            if reaccion.tipo == tipo:
                reaccion.delete()
                mensaje = 'Reacción removida'
            else:
                reaccion.tipo = tipo
                reaccion.save()
                mensaje = 'Reacción actualizada'
        else:
            mensaje = 'Reacción registrada'

        conteo = Publicacion.objects.filter(pk=publicacion.pk).aggregate(
            likes=Count('reacciones', filter=Q(reacciones__tipo='like')),
            dislikes=Count('reacciones', filter=Q(reacciones__tipo='dislike')),
        )
        Publicacion.objects.filter(pk=publicacion.pk).update(
            likes_count=conteo['likes'],
            dislikes_count=conteo['dislikes'],
        )

        return Response({'mensaje': mensaje})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated()])
    def comentarios(self, request, pk=None):
        publicacion = self.get_object()
        serializer = ComentarioCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comentario = Comentario.objects.create(
            publicacion=publicacion,
            usuario_id=request.user.id,
            texto=serializer.validated_data['texto']
        )

        result = ComentarioSerializer(
            Comentario.objects.select_related('usuario').get(pk=comentario.pk)
        )
        return Response({'mensaje': 'Comentario agregado', 'comentario': result.data},
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='comentarios/(?P<comentario_id>[^/.]+)',
            permission_classes=[IsAuthenticated()])
    def eliminar_comentario(self, request, comentario_id=None):
        try:
            comentario = Comentario.objects.get(pk=comentario_id)
        except Comentario.DoesNotExist:
            return Response({'error': 'Comentario no encontrado'},
                            status=status.HTTP_404_NOT_FOUND)

        if comentario.usuario_id != request.user.id:
            return Response({'error': 'No puedes eliminar este comentario'},
                            status=status.HTTP_403_FORBIDDEN)

        comentario.delete()
        return Response({'mensaje': 'Comentario eliminado'})
