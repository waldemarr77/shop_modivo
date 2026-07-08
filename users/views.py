from rest_framework import viewsets
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(username=self.request.user.username)
    

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    