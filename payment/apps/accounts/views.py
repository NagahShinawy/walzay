from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
