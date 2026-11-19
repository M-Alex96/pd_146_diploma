from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from backend.models import *

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password', 'type']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            last_name=validated_data.get('last_name', ''),
            first_name=validated_data.get('first_name', ''),
            type=validated_data.get('type', 'buyer'),
        )
        return user

class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name']

class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer(read_only=True)
    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'state']

class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(many=True, read_only=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters']

class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(read_only=True)
    product_info_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductInfo.objects.all(),
        source='product_info',
        write_only=True
    )
    sum = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_info', 'product_info_id', 'quantity', 'sum']

    def get_sum(self, obj):
        return obj.quantity * obj.product_info.price

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_sum = serializers.SerializerMethodField()
    contact = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'dt', 'status', 'order_items', 'total_sum', 'contact']

    def get_total_sum(self, obj):
        return obj.total_sum

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'last_name', 'first_name', 'middle_name', 'email',
            'phone', 'address', 'city', 'street', 'house', 'building', 'structure', 'apartment',
        ]