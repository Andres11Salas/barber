from rest_framework.routers import SimpleRouter
from .views import UsuarioViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', UsuarioViewSet)

urlpatterns = router.urls
