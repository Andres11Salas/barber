from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    re_path(r'^api/auth(?:/|$)', include('apps.authentication.urls')),
    re_path(r'^api/usuarios(?:/|$)', include('apps.usuarios.urls')),
    re_path(r'^api/usuarios/', include('apps.usuarios.urls')),
    re_path(r'^api/servicios(?:/|$)', include('apps.servicios.urls')),
    re_path(r'^api/citas(?:/|$)', include('apps.citas.urls')),
    re_path(r'^api/publicaciones(?:/|$)', include('apps.publicaciones.urls')),
    re_path(r'^api/pagos(?:/|$)', include('apps.pagos.urls')),
]

public_dir = settings.BASE_DIR / 'public'
if public_dir.exists():
    urlpatterns += [
        path('', serve, {'document_root': str(public_dir), 'path': 'index.html'}),
        re_path(r'^styles/(?P<path>.*)$', serve, {
            'document_root': str(public_dir / 'styles')
        }),
        re_path(r'^(?P<path>.*\.(css|js|png|jpg|jpeg|gif|ico|svg|woff2?|ttf|eot))$', serve, {
            'document_root': str(public_dir)
        }),
        re_path(r'^(?P<path>.*)$', serve, {
            'document_root': str(public_dir)
        }),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
