from rest_framework.routers import SimpleRouter
from .views import PublicacionViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', PublicacionViewSet)

urlpatterns = router.urls
