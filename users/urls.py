from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserUpdateAPIView, PaymentListAPIView, UserRetrieveAPIView, UserDestroyAPIView, UserListAPIView, RegisterAPIView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("profiles/<int:pk>/update/", UserUpdateAPIView.as_view(), name="profile-update"),
    path("profiles/<int:pk>/", UserRetrieveAPIView.as_view(), name="profile"),
    path("profiles/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="profile-delete"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("profiles/", UserListAPIView.as_view(), name="user-list"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
