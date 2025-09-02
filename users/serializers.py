from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"

class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payments"""

    user_name = serializers.EmailField(source="user.email", read_only=True)
    course_name = serializers.CharField(source="course.email", read_only=True, allow_null=True)
    lesson_name = serializers.CharField(source="lesson.email", read_only=True, allow_null=True)

    name_product = serializers.CharField(read_only=True)
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payments
        fields = "__all__"

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)

        token["email"] = user.email

        return token
