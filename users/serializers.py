from rest_framework import serializers
from .models import CustomUser, Payment
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    payments_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["email", "phone_number", "city", "full_name", "avatar", "password", "payments_count"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(**validated_data)

    def get_payments_count(self, obj):
        return obj.payment.count()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password", "full_name", "payments_count"]


class PaymentSerializer(serializers.ModelSerializer):

    payment_history = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = '__all__'

