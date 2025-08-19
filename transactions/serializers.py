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

        # getting additional infos
        request = self.context["request"]
        view = self.context.get("view")
        user = request.user

        # if a request contains a url parameter called id
        id = view.kwargs.get("pk")

        # checking if id exists then the request is a update request so we should get infos like amount and date from database because it may change in update request
        if id:
            transaction = Transaction.objects.get(id=id)

            if not data.get("type"):
                data["type"] = transaction.type

            data["amount"] = transaction.amount
            data["date"] = transaction.date

        # if transaction type is a expense it will get budgets in that date range to check if limit is hit or not
        if data["type"] == "expense":
            budgets = user.budget_set.filter(
                start_date__lte=data["date"], end_date__gte=data["date"]
            )
            for budget in budgets:

                message = budget.check_limit(data["amount"])

                # if sending notifications is failed it will set a context variable to true so we can send warning to user with response
                if not message:
                    self.context["notif_not_sent"] = True

        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        message_sent = self.context.get("notif_not_sent")

        if message_sent:
            rep.update({"warning": "failed to send notification, budget exceeded!"})

        return rep
