from rest_framework import generics
from .serializers import UserSerializer
from .models import CustomUser

# Create your views here.

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
