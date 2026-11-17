from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from backend.models import *
from backend.serializers import ShopSerializer, ObtainTokenPairSerializer, RegistrationSerializer

class RegistrationView(APIView):
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

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
