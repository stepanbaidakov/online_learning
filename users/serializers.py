from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments_history = PaymentSerializer(source="payment", read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ["email", "phone_number", "city", "full_name", "avatar", "password", "payments_history"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    payments_history = PaymentSerializer(source="payment", read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ["id", "password", "full_name", "payments_history", "email"]
        extra_kwargs = {"password": {"write_only": True}}


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        self.user.last_login = timezone.now()
        self.user.save(update_fields=["last_login"])

        return data
