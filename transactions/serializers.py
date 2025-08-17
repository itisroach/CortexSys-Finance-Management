from rest_framework import serializers
from .models import Transaction
from rest_framework.exceptions import PermissionDenied


class TransactionSerializer(serializers.ModelSerializer):

    date = serializers.DateField("%Y-%m-%d")

    class Meta:

        model = Transaction
        fields = [
            "id",
            "title",
            "amount",
            "type",
            "date",
            "notes",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):

        request = self.context.get("request")

        user = request.user

        validated_data["user_id"] = user

        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def validate(self, data):

        request = self.context["request"]
        view = self.context.get("view")
        user = request.user

        id = view.kwargs.get("pk")

        if id:
            transaction = Transaction.objects.get(id=id)

            if not data.get("type"):
                data["type"] = transaction.type

            data["amount"] = transaction.amount
            data["date"] = transaction.date

        if data["type"] == "expense":
            budgets = user.budget_set.filter(
                start_date__lte=data["date"], end_date__gte=data["date"]
            )
            for budget in budgets:

                message = budget.check_limit(data["amount"])

                if message:
                    raise PermissionDenied(message)

        return data
