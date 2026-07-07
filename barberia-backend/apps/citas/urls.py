from rest_framework.routers import SimpleRouter
from .views import CitaViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', CitaViewSet)

urlpatterns = router.urls
