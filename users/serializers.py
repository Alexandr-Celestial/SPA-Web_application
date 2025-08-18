from rest_framework import serializers

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"

class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payments"""

    class Meta:
        model = Payments
        fields = "__all__"