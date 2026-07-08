from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Cita
from apps.usuarios.serializers import UsuarioPerfilSerializer
from apps.servicios.serializers import ServicioSerializer


class CitaSerializer(serializers.ModelSerializer):
    cliente = UsuarioPerfilSerializer(read_only=True)
    barbero = UsuarioPerfilSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)
    cliente_id = serializers.IntegerField(write_only=True)
    barbero_id = serializers.IntegerField(write_only=True)
    servicio_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cita
        fields = ['id', 'cliente', 'barbero', 'servicio', 'cliente_id', 'barbero_id',
                  'servicio_id', 'fecha', 'hora', 'estado', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
            'estado': {'read_only': True},
        }

    def validate(self, data):
        barbero = data.get('barbero_id')
        fecha = data.get('fecha')
        hora = data.get('hora')
        servicio_id = data.get('servicio_id')

        duracion = 30
        if servicio_id:
            from apps.servicios.models import Servicio
            try:
                servicio = Servicio.objects.get(id=servicio_id)
                duracion = servicio.duracion_minutos or 30
            except Servicio.DoesNotExist:
                pass

        hora_inicio = datetime.combine(fecha, hora)
        hora_fin = hora_inicio + timedelta(minutes=duracion)

        citas_existentes = Cita.objects.filter(
            barbero_id=barbero,
            fecha=fecha,
            estado__in=['PENDIENTE', 'COMPLETADA']
        )

        for cita in citas_existentes:
            cita_inicio = datetime.combine(cita.fecha, cita.hora)
            cita_duracion = 30
            if cita.servicio_id:
                from apps.servicios.models import Servicio
                try:
                    cita_serv = Servicio.objects.get(id=cita.servicio_id)
                    cita_duracion = cita_serv.duracion_minutos or 30
                except Servicio.DoesNotExist:
                    pass
            cita_fin = cita_inicio + timedelta(minutes=cita_duracion)

            if hora_inicio < cita_fin and hora_fin > cita_inicio:
                raise serializers.ValidationError(
                    'El barbero ya tiene una cita en ese horario. Por favor elige otra hora o fecha.'
                )

        if hora_inicio <= datetime.now():
            raise serializers.ValidationError('No puedes agendar citas en el pasado.')

        return data
