from rest_framework import serializers
from .models import CustomUser, Payment
from django.contrib.auth import get_user_model


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


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
