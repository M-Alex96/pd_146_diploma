from rest_framework.routers import DefaultRouter
from backend.views import ShopViewSet, ProductInfoViewSet, OrderViewSet

router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductInfoViewSet)
router.register('orders', OrderViewSet)

urlpatterns = router.urls