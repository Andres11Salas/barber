from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Cita
from apps.usuarios.serializers import UsuarioPerfilSerializer
from apps.servicios.serializers import ServicioSerializer
from apps.servicios.models import Servicio


class CitaSerializer(serializers.ModelSerializer):
    cliente = UsuarioPerfilSerializer(read_only=True)
    barbero = UsuarioPerfilSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)
    servicios_adicionales = ServicioSerializer(many=True, read_only=True)
    cliente_id = serializers.IntegerField(write_only=True, required=False)
    barbero_id = serializers.IntegerField(write_only=True)
    servicio_id = serializers.IntegerField(write_only=True)
    servicios_adicionales_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False, default=list
    )
    servicios_nombres = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = ['id', 'cliente', 'barbero', 'servicio', 'servicios_adicionales',
                  'cliente_id', 'barbero_id', 'servicio_id', 'servicios_adicionales_ids',
                  'fecha', 'hora', 'duracion_total', 'estado',
                  'createdAt', 'updatedAt', 'servicios_nombres']
        extra_kwargs = {
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
            'estado': {'read_only': True},
            'duracion_total': {'read_only': True},
        }

    def get_servicios_nombres(self, obj):
        nombres = [obj.servicio.nombre]
        for s in obj.servicios_adicionales.all():
            nombres.append(s.nombre)
        return ', '.join(nombres)

    def compute_duracion(self, servicio_id, adicionales_ids):
        duracion = 30
        try:
            s = Servicio.objects.get(id=servicio_id)
            duracion = s.duracion_minutos or 30
        except Servicio.DoesNotExist:
            pass
        for sid in (adicionales_ids or []):
            try:
                s = Servicio.objects.get(id=sid)
                duracion += s.duracion_minutos or 0
            except Servicio.DoesNotExist:
                pass
        return duracion

    def validate(self, data):
        barbero = data.get('barbero_id')
        fecha = data.get('fecha')
        hora = data.get('hora')
        servicio_id = data.get('servicio_id')
        adicionales_ids = data.get('servicios_adicionales_ids', [])

        if not servicio_id:
            raise serializers.ValidationError('Debes seleccionar al menos un servicio principal.')

        if fecha.weekday() >= 5:
            raise serializers.ValidationError('Solo atendemos de lunes a viernes. Elige un día hábil.')

        if hora.hour < 10 or hora.hour >= 19:
            raise serializers.ValidationError('El horario de atención es de 10:00 a 19:00.')

        duracion = self.compute_duracion(servicio_id, adicionales_ids)

        hora_inicio = datetime.combine(fecha, hora)
        hora_fin = hora_inicio + timedelta(minutes=duracion)

        if hora_fin.hour > 19 or (hora_fin.hour == 19 and hora_fin.minute > 0):
            raise serializers.ValidationError('La cita excede el horario de atención (cierre 19:00). Elige una hora más temprana.')

        citas_existentes = Cita.objects.filter(
            barbero_id=barbero,
            fecha=fecha,
            estado__in=['PENDIENTE', 'COMPLETADA']
        )

        for cita in citas_existentes:
            cita_inicio = datetime.combine(cita.fecha, cita.hora)
            cita_fin = cita_inicio + timedelta(minutes=cita.duracion_total or 30)

            if hora_inicio < cita_fin and hora_fin > cita_inicio:
                raise serializers.ValidationError(
                    'El barbero ya tiene una cita en ese horario.'
                )

        if hora_inicio <= datetime.now():
            raise serializers.ValidationError('No puedes agendar citas en el pasado.')

        data['duracion_total'] = duracion
        return data

    def create(self, validated_data):
        adicionales_ids = validated_data.pop('servicios_adicionales_ids', [])
        duracion = validated_data.pop('duracion_total', 30)
        cita = Cita.objects.create(**validated_data, duracion_total=duracion)
        if adicionales_ids:
            cita.servicios_adicionales.set(adicionales_ids)
        return cita