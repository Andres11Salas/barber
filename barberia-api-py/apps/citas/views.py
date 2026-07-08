from datetime import datetime, date, timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Cita
from .serializers import CitaSerializer
from apps.usuarios.models import Usuario
from apps.usuarios.serializers import UsuarioPerfilSerializer
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

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def barberos_disponibles(self, request):
        fecha_str = request.query_params.get('fecha')
        servicio_id = request.query_params.get('servicio_id')

        if not fecha_str or not servicio_id:
            return Response({'error': 'fecha y servicio_id son requeridos'}, status=400)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Formato de fecha invalido. Use YYYY-MM-DD'}, status=400)

        from apps.servicios.models import Servicio
        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            return Response({'error': 'Servicio no encontrado'}, status=404)

        duracion = servicio.duracion_minutos or 30
        barberos = Usuario.objects.filter(rol__in=['BARBERO', 'ADM'], estado='ACTIVO')

        barberos_disponibles = []
        for barbero in barberos:
            citas_hoy = Cita.objects.filter(
                barbero_id=barbero.id,
                fecha=fecha,
                estado__in=['PENDIENTE', 'COMPLETADA']
            )
            barberos_disponibles.append({
                'id': barbero.id,
                'nombre': barbero.nombre,
                'email': barbero.email,
                'telefono': barbero.telefono,
                'bio': barbero.bio,
                'citas_count': citas_hoy.count(),
            })

        return Response({
            'fecha': fecha_str,
            'servicio': servicio.nombre,
            'duracion_minutos': duracion,
            'barberos': barberos_disponibles
        })

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def horarios_disponibles(self, request):
        fecha_str = request.query_params.get('fecha')
        barbero_id = request.query_params.get('barbero_id')
        servicio_id = request.query_params.get('servicio_id')

        if not all([fecha_str, barbero_id, servicio_id]):
            return Response({'error': 'fecha, barbero_id y servicio_id son requeridos'}, status=400)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Formato de fecha invalido'}, status=400)

        from apps.servicios.models import Servicio
        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            return Response({'error': 'Servicio no encontrado'}, status=404)

        duracion = servicio.duracion_minutos or 30
        apertura = 8
        cierre = 20
        intervalos = []

        citas_ocupadas = Cita.objects.filter(
            barbero_id=barbero_id,
            fecha=fecha,
            estado__in=['PENDIENTE', 'COMPLETADA']
        )

        hora_actual = datetime.now()
        for hora in range(apertura, cierre):
            hora_slot = datetime.combine(fecha, datetime.strptime(f'{hora}:00', '%H:%M').time())
            if fecha == date.today() and hora_slot <= hora_actual + timedelta(hours=1):
                continue

            slot_inicio = hora_slot
            slot_fin = slot_inicio + timedelta(minutes=duracion)
            ocupado = False

            for cita in citas_ocupadas:
                cita_inicio = datetime.combine(cita.fecha, cita.hora)
                cita_duracion = 30
                if cita.servicio_id:
                    try:
                        cita_serv = Servicio.objects.get(id=cita.servicio_id)
                        cita_duracion = cita_serv.duracion_minutos or 30
                    except Servicio.DoesNotExist:
                        pass
                cita_fin = cita_inicio + timedelta(minutes=cita_duracion)
                if slot_inicio < cita_fin and slot_fin > cita_inicio:
                    ocupado = True
                    break

            if not ocupado:
                hora_label = f'{hora:02d}:00'
                intervalos.append({
                    'hora': hora_label,
                    'display': f'{hora:02d}:00 - {(hora+duracion//60):02d}:{duracion%60:02d}'
                })

        return Response({'horarios': intervalos})

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
