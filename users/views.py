from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .serializers import UserSerializer, PaymentSerializer
from .models import CustomUser, Payment
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["date"]
    filterset_fields = ["method", "course", "lesson"]
