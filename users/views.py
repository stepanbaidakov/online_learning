from rest_framework import generics
from .models import CustomUser

# Create your views here.

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUser
    queryset = CustomUser.objects.all()
