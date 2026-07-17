from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CreatePaymentAPIView,
    CustomTokenObtainPairView,
    PaymentListAPIView,
    PaymentStatusAPIView,
    RegisterAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = "users"

urlpatterns = [
    path("profiles/<int:pk>/update/", UserUpdateAPIView.as_view(), name="profile-update"),
    path("profiles/<int:pk>/", UserRetrieveAPIView.as_view(), name="profile"),
    path("profiles/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="profile-delete"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("profiles/", UserListAPIView.as_view(), name="user-list"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payments/status/<str:session_id>/", PaymentStatusAPIView.as_view(), name="payment-status"),
    path("payments/create/<int:pk>/", CreatePaymentAPIView.as_view(), name="payment-create"),
]
