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
from materials.models import Course
from django.urls import reverse_lazy

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
        course = Course.objects.get(pk=kwargs.get("pk"))
        api_key = os.getenv("API_KEY")
        client = StripeClient(api_key)

        product = client.v1.products.create({
            "name": course.title
        })
        price = client.v1.prices.create({
            "product": product.id,
            "unit_amount": int(course.price * 100),
            "currency": "usd"
        })

        session = client.v1.checkout.sessions.create({
            "success_url": f"http://localhost:8000/courses/{course.id}/",
            "line_items": [{"price": price.id, "quantity": 1}],
            "mode": "payment",
        })
        Payment.objects.create(
            user=request.user,
            course=course,
            amount=session.amount_total,
            status="unpaid",
            stripe_session_id=session.id,
        )

        payment_status = reverse_lazy("users:payment-status", kwargs={"session_id": session.id})
        return Response({"checkout_url": session.url, "payment_status_url": payment_status})


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
