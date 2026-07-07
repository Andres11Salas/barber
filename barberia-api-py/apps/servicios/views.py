from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Servicio
from .serializers import ServicioSerializer
from apps.usuarios.permissions import EsAdmin


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), EsAdmin()]
        return [AllowAny()]
