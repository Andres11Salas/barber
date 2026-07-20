from django.db import models


class Publicacion(models.Model):
    id = models.AutoField(primary_key=True)
    barbero = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.CASCADE,
        related_name='publicaciones', db_column='barbero_id'
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    contenido_json = models.JSONField(blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'publicaciones'
        ordering = ['-createdAt']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    publicacion = models.ForeignKey(
        Publicacion, on_delete=models.CASCADE,
        related_name='comentarios', db_column='publicacion_id'
    )
    usuario = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.CASCADE,
        related_name='comentarios_realizados', db_column='usuario_id'
    )
    texto = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'comentarios'
        ordering = ['-createdAt']

    def __str__(self):
        return f"Comentario de {self.usuario_id} en #{self.publicacion_id}"


class Reaccion(models.Model):
    TIPOS = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    id = models.AutoField(primary_key=True)
    publicacion = models.ForeignKey(
        Publicacion, on_delete=models.CASCADE,
        related_name='reacciones', db_column='publicacion_id'
    )
    usuario = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.CASCADE,
        related_name='reacciones_realizadas', db_column='usuario_id'
    )
    tipo = models.CharField(max_length=10, choices=TIPOS)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        db_table = 'reacciones'
        constraints = [
            models.UniqueConstraint(
                fields=['publicacion', 'usuario'],
                name='unique_publicacion_usuario'
            )
        ]

    def __str__(self):
        return f"{self.tipo} de {self.usuario_id} en #{self.publicacion_id}"
