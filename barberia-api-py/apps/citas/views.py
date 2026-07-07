from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Cita
from .serializers import CitaSerializer
from apps.usuarios.permissions import EsCliente


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.select_related('cliente', 'barbero', 'servicio').all()
    serializer_class = CitaSerializer

    def get_permissions(self):
        if self.action == 'cancelar_cliente':
            return [IsAuthenticated(), EsCliente()]
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['delete'], url_path='cliente/(?P<pk>[^/.]+)')
    def cancelar_cliente(self, request, pk=None):
        try:
            cita = Cita.objects.get(pk=pk)
        except Cita.DoesNotExist:
            return Response({'error': 'Cita no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if cita.cliente_id != request.user.id:
            return Response(
                {'error': 'No tienes permiso para cancelar esta cita.'},
                status=status.HTTP_403_FORBIDDEN
            )

        fecha_cita = datetime.combine(cita.fecha, cita.hora)
        fecha_cita = timezone.make_aware(fecha_cita) if timezone.is_naive(fecha_cita) else fecha_cita
        ahora = timezone.now()
        horas_diferencia = (fecha_cita - ahora).total_seconds() / 3600

        if horas_diferencia < 6:
            return Response(
                {'error': 'Debes cancelar con al menos 6 horas de anticipación. Por favor, comunícate con la barbería.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cita.delete()
        return Response({'mensaje': 'Tu cita ha sido cancelada exitosamente.'})
