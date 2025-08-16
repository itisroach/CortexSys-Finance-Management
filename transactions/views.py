from django.shortcuts import render
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated

class TransactionsView(viewsets.ModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = Transaction.objects.filter(user_id=self.request.user.id)

        return queryset
