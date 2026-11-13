from django.shortcuts import render
from rest_framework import viewsets
from backend.models import *
from backend.serializers import ShopSerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer