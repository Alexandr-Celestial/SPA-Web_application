from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import Payments, User
from users.permissions import OwnerOnlyPerm
from users.serializers import PaymentsSerializer, UserSerializer


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def my_protected_view(request):
#     # Ваш код представления
#     return Response({'message': 'Авторизовано!'})


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyPerm]

class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyPerm]
    queryset = User.objects.all()

class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyPerm]
