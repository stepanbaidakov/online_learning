from .views import UserUpdateAPIView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("profile/<int:pk>/update", UserUpdateAPIView.as_view(), name="profile_update"),
]
