from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import Payments, User, Subscription
from users.permissions import OwnerOnlyPerm
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import create_stripe_price_amount, create_stripe_session


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

class SubscriptionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({'message': message})

class CreateProductPrice(CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        pay = serializer.save(user=self.request.user)
        price = create_stripe_price_amount(pay.name_product, pay.amount)
        session_id, session_link = create_stripe_session(price)
        pay.session_id = session_id
        pay.link = session_link
        pay.save()
