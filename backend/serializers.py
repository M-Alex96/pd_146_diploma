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

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'state']

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['product', 'shop', 'quantity', 'price', 'price_rrc']