from django.db import models


class Pago(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('PENDIENTE_REEMBOLSO', 'Pendiente de reembolso'),
        ('REEMBOLSADO', 'Reembolsado'),
    ]

    id = models.AutoField(primary_key=True)
    cita = models.ForeignKey(
        'citas.Cita', on_delete=models.CASCADE,
        related_name='pagos', db_column='cita_id'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    mercadopago_id = models.CharField(max_length=255, null=True, blank=True)
    preference_id = models.CharField(max_length=255, null=True, blank=True)
    metodo_pago = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        db_table = 'pagos'
        ordering = ['-createdAt']

    def __str__(self):
        return f"Pago #{self.id} - {self.monto} ({self.estado})"