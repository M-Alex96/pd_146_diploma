from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from backend.views import ShopViewSet, ProductInfoViewSet, OrderViewSet, ContactViewSet, ObtainTokenPairView, \
    RegistrationView, PartnerUpdate

router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductInfoViewSet)
router.register('orders', OrderViewSet)
router.register('contacts', ContactViewSet)

urlpatterns = [
    path('login/', ObtainTokenPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update')
] + router.urls