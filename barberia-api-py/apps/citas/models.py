from django.db import models


class Cita(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.CASCADE,
        related_name='citas_como_cliente', db_column='cliente_id'
    )
    barbero = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.CASCADE,
        related_name='citas_como_barbero', db_column='barbero_id'
    )
    servicio = models.ForeignKey(
        'servicios.Servicio', on_delete=models.CASCADE,
        related_name='citas', db_column='servicio_id'
    )
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        db_table = 'citas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"Cita #{self.id} - {self.fecha} {self.hora}"
