from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    date = serializers.DateField("%Y-%m-%d")

    class Meta:

        model = Transaction
        fields = ["id", "title", "amount","type", "date", "notes"]


    def create(self, validated_data):

        request = self.context.get("request")

        user = request.user

        validated_data["user_id"] = user

        transaction = Transaction.objects.create(**validated_data)
        return transaction
    