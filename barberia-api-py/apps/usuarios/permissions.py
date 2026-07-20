from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'ADM'


class EsBarbero(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'BARBERO'


class EsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'CLIENTE'


class EsBarberoOAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol in ('BARBERO', 'ADM')


class EsPropietarioOAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.rol == 'ADM':
            return True
        if hasattr(obj, 'cliente_id'):
            return obj.cliente_id == request.user.id
        if hasattr(obj, 'usuario_id'):
            return obj.usuario_id == request.user.id
        if hasattr(obj, 'barbero_id'):
            return obj.barbero_id == request.user.id
        return obj.id == request.user.id
