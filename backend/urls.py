from rest_framework.routers import DefaultRouter
from backend.views import ShopViewSet, ProductInfoViewSet, OrderViewSet, ContactViewSet

router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductInfoViewSet)
router.register('orders', OrderViewSet)
router.register('contacts', ContactViewSet)

urlpatterns = router.urls