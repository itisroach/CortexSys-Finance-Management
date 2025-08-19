from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from .serializers import AccountSerializer, DeviceTokenSerializer
from accounts.models import Account
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(CreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [AllowAny]


class DeviceTokenViewSet(ModelViewSet):
    serializer_class = DeviceTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.device_tokens.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
