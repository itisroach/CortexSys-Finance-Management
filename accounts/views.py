from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import AccountSerializer
from accounts.models import Account
from rest_framework.permissions import AllowAny


class RegisterView(CreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [AllowAny]
