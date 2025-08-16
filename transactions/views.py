from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TransactionsView(viewsets.ModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()

    def get_queryset(self):

        query = self.request.query_params.get("type")
            
        queryset = super().get_queryset()

        if not query:
            queryset = Transaction.objects.filter(user_id=self.request.user.id)

        else:
            queryset = Transaction.objects.filter(user_id=self.request.user.id, type=query)

        return queryset
    

    @action(detail=False, methods=['get'])
    def report(self, request):
        user = request.user
        balance, income, expense = user.balance()



        return Response({
            'total_income': income,
            'total_expense': expense,
            'balance': balance,
        })
