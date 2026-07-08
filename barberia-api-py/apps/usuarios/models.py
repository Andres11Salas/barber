from django.db import models


class Usuario(models.Model):
    ROLES = [
        ('ADM', 'Administrador'),
        ('BARBERO', 'Barbero'),
        ('CLIENTE', 'Cliente'),
    ]
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        db_table = 'usuarios'
        ordering = ['-createdAt']

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
