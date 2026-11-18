from rest_framework.routers import DefaultRouter
from backend.views import ShopViewSet, ProductInfoViewSet

router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductInfoViewSet)

urlpatterns = router.urls