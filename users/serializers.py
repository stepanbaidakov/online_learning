from rest_framework import serializers
from .models import CustomUser, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    payment_history = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_history(self, obj):
        return obj.user.payment.count()
