from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register-user"),
    path("login/", TokenObtainPairView.as_view(), name="login-user"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
]
