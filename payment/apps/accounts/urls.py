from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserRegisterAPIView, UserListView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user_list'),

]
