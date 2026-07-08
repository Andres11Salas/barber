from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import EsAdmin


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [IsAuthenticated(), EsAdmin()]
        if self.action in ('update', 'partial_update'):
            if self.request.user and self.kwargs.get('pk') == str(self.request.user.pk):
                return [IsAuthenticated()]
            return [IsAuthenticated(), EsAdmin()]
        return [AllowAny()]
