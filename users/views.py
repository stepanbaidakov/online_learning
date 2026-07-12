from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsOwner
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .serializers import UserSerializer, PaymentSerializer, UserListSerializer
from .models import CustomUser, Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
import os
from stripe import StripeClient
from rest_framework_simplejwt.views import TokenObtainPairView
from .services import create_checkout_session
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["date"]
    filterset_fields = ["method", "course", "lesson"]


class CreatePaymentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        result = create_checkout_session(request, *args, **kwargs)
        return result


class PaymentStatusAPIView(APIView):
    def get(self, request, session_id):
        client = StripeClient(os.getenv("API_KEY"))

        session = client.v1.checkout.sessions.retrieve(session_id)
        payment = Payment.objects.get(
            stripe_session_id=session_id
        )

        payment.status = session.payment_status
        payment.save()

        return Response({
            "status": payment.status,
            "amount": payment.amount,
            "course": payment.course.title,
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer