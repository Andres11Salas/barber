from rest_framework.routers import SimpleRouter
from .views import ServicioViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', ServicioViewSet)

urlpatterns = router.urls
