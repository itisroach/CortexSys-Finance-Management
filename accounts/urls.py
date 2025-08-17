from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register-user"),
    path("login/", TokenObtainPairView.as_view(), name="login-user"),
]
