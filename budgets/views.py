from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import BudgetSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Budget



class BudgetViewset(ModelViewSet):

    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated,]
    queryset = Budget.objects.all()


    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = Budget.objects.filter(user_id=self.request.user.id)

        return queryset