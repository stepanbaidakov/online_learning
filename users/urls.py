from .views import UserUpdateAPIView, PaymentListAPIView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("profile/<int:pk>/update", UserUpdateAPIView.as_view(), name="profile-update"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]
