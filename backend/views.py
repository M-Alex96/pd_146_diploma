from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import yaml
from backend.filters import ProductInfoFilter
from backend.models import *
from backend.serializers import ShopSerializer, ObtainTokenPairSerializer, RegistrationSerializer, \
    ProductInfoSerializer, OrderSerializer, ContactSerializer


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if not url:
            return Response({'Status': False, 'Error': 'Не указан url'}, status=400)

        try:
            URLValidator()(url)
        except ValidationError:
            return Response({'Status': False, 'Error': 'Некорректный url'}, status=400)

        try:
            response = requests.get(url)
            data = yaml.safe_load(response.content)
        except Exception as e:
            return Response({'Status': False, 'Error': f'Ошибка загрузки файла: {e}'}, status=400)

        shop, _ = Shop.objects.get_or_create(
            name=data['shop'],
            defaults={'url': url, 'state': True}
        )

        if not request.user.shop:
            request.user.shop = shop
            request.user.save()

        ProductInfo.objects.filter(shop=shop).delete()

        for cat in data.get('categories', []):
            category, _ = Category.objects.get_or_create(
                id=cat['id'],
                defaults={'name': cat['name']}
            )
            category.shops.add(shop)

        for good in data.get('goods', []):
            product, _ = Product.objects.get_or_create(
                name=good['name'],
                defaults={
                    'category_id': good['category'],
                    'model': good.get('model', ''),
                    'description': ''
                }
            )

            product_info = ProductInfo.objects.create(
                product=product,
                shop=shop,
                quantity=good['quantity'],
                price=good['price'],
                price_rrc=good['price_rrc']
            )

            for name, value in good.get('parameters', {}).items():
                parameter, _ = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.create(
                    product_info=product_info,
                    parameter=parameter,
                    value=str(value)
                )

        return Response({'Status': True, 'Message': 'Прайс успешно загружен'})


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer

class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer
    permission_classes = [AllowAny]

class ProductInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductInfoFilter

    def get_queryset(self):
        return ProductInfo.objects.select_related(
            'product', 'shop', 'product__category'
        ).prefetch_related(
            'product_parameters__parameter'
        ).filter(shop__state=True, quantity__gt=0)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)