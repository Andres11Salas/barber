from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer, ActualizarPerfilSerializer
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

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def mi_perfil(self, request):
        serializer = ActualizarPerfilSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UsuarioSerializer(request.user).data)
        return Response(serializer.errors, status=400)
