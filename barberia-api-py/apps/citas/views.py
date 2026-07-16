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


def es_dia_habil(fecha):
    return fecha.weekday() < 5


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.select_related('cliente', 'barbero', 'servicio').prefetch_related('servicios_adicionales').all()
    serializer_class = CitaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            if user.rol == 'CLIENTE':
                qs = qs.filter(cliente_id=user.id)
            elif user.rol == 'BARBERO':
                qs = qs.filter(barbero_id=user.id)
        return qs

    def perform_create(self, serializer):
        serializer.save(cliente_id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'cancelar_cliente':
            return [IsAuthenticated(), EsCliente()]
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def tiempo_servicios(self, request):
        servicio_ids = request.query_params.getlist('servicio_ids[]') or request.query_params.getlist('servicio_ids')
        ids = [int(x) for x in servicio_ids if x.isdigit()]
        if not ids:
            return Response({'error': 'servicio_ids requerido'}, status=400)
        from apps.servicios.models import Servicio
        servicios = Servicio.objects.filter(id__in=ids)
        total = sum(s.duracion_minutos or 0 for s in servicios)
        return Response({
            'servicios': [{'id': s.id, 'nombre': s.nombre, 'duracion_minutos': s.duracion_minutos} for s in servicios],
            'duracion_total': total,
            'minutos': total
        })

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def barberos_disponibles(self, request):
        fecha_str = request.query_params.get('fecha')
        duracion = request.query_params.get('duracion')

        if not fecha_str or not duracion:
            return Response({'error': 'fecha y duracion son requeridos'}, status=400)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Formato de fecha invalido. Use YYYY-MM-DD'}, status=400)

        if not es_dia_habil(fecha):
            return Response({'error': 'Solo atendemos de lunes a viernes.'}, status=400)

        try:
            duracion = int(duracion)
        except ValueError:
            return Response({'error': 'duracion debe ser un número'}, status=400)

        barberos = Usuario.objects.filter(rol__in=['BARBERO', 'ADM'], estado='ACTIVO')

        resultado = []
        APERTURA = 10
        CIERRE = 19
        hora_actual = datetime.now()

        for barbero in barberos:
            citas_ocupadas = Cita.objects.filter(
                barbero_id=barbero.id, fecha=fecha,
                estado__in=['PENDIENTE', 'COMPLETADA']
            )

            slots = []
            for h in range(APERTURA, CIERRE):
                hora_slot = datetime.combine(fecha, datetime.strptime(f'{h}:00', '%H:%M').time())
                pasado = fecha == date.today() and hora_slot <= hora_actual + timedelta(hours=1)
                slot_inicio = hora_slot
                slot_fin = slot_inicio + timedelta(minutes=duracion)
                excede = slot_fin.hour > CIERRE or (slot_fin.hour == CIERRE and slot_fin.minute > 0)
                ocupado = pasado or excede
                if not ocupado:
                    for cita in citas_ocupadas:
                        c_inicio = datetime.combine(cita.fecha, cita.hora)
                        c_fin = c_inicio + timedelta(minutes=cita.duracion_total or 30)
                        if slot_inicio < c_fin and slot_fin > c_inicio:
                            ocupado = True
                            break
                slots.append({
                    'hora': f'{h:02d}:00',
                    'disponible': not ocupado,
                    'pasado': pasado,
                    'excede': excede,
                })

            resultado.append({
                'id': barbero.id,
                'nombre': barbero.nombre,
                'email': barbero.email,
                'telefono': barbero.telefono,
                'bio': barbero.bio,
                'citas_count': citas_ocupadas.count(),
                'espacios_libres': [s['hora'] for s in slots if s['disponible']],
                'slots': slots,
            })

        return Response(resultado)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def horarios_disponibles(self, request):
        fecha_str = request.query_params.get('fecha')
        barbero_id = request.query_params.get('barbero_id')
        duracion = request.query_params.get('duracion')

        if not all([fecha_str, barbero_id, duracion]):
            return Response({'error': 'fecha, barbero_id y duracion son requeridos'}, status=400)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Formato de fecha invalido'}, status=400)

        if not es_dia_habil(fecha):
            return Response({'error': 'Solo atendemos de lunes a viernes.'}, status=400)

        try:
            duracion = int(duracion)
        except ValueError:
            return Response({'error': 'duracion debe ser un número'}, status=400)

        APERTURA = 10
        CIERRE = 19
        intervalos = []

        citas_ocupadas = Cita.objects.filter(
            barbero_id=barbero_id, fecha=fecha,
            estado__in=['PENDIENTE', 'COMPLETADA']
        )

        hora_actual = datetime.now()
        for h in range(APERTURA, CIERRE):
            hora_slot = datetime.combine(fecha, datetime.strptime(f'{h}:00', '%H:%M').time())
            if fecha == date.today() and hora_slot <= hora_actual + timedelta(hours=1):
                continue

            slot_inicio = hora_slot
            slot_fin = slot_inicio + timedelta(minutes=duracion)

            if slot_fin.hour > CIERRE or (slot_fin.hour == CIERRE and slot_fin.minute > 0):
                continue

            ocupado = False
            for cita in citas_ocupadas:
                c_inicio = datetime.combine(cita.fecha, cita.hora)
                c_fin = c_inicio + timedelta(minutes=cita.duracion_total or 30)
                if slot_inicio < c_fin and slot_fin > c_inicio:
                    ocupado = True
                    break

            if not ocupado:
                fin = slot_fin
                intervalos.append({
                    'hora': f'{h:02d}:00',
                    'display': f'{h:02d}:00 - {fin.hour:02d}:{fin.minute:02d}'
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

        if horas_diferencia < 3:
            return Response(
                {'error': 'Debes cancelar con al menos 3 horas de anticipación.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cita.estado = 'CANCELADA'
        cita.save()
        return Response({'mensaje': 'Tu cita ha sido cancelada exitosamente.'})