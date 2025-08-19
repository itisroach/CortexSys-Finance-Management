from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import DeviceTokenViewSet

router = DefaultRouter()
router.register(r"device-tokens", DeviceTokenViewSet, basename="device-token")

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register-user"),
    path("login/", TokenObtainPairView.as_view(), name="login-user"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
] + router.urls
