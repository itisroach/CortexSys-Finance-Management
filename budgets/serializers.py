from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):

    start_date = serializers.DateField("%Y-%m-%d")
    end_date = serializers.DateField("%Y-%m-%d")

    class Meta:

        model = Budget
        fields = ["id", "title", "total_amount", "start_date", "end_date"]


    def create(self, validated_data):

        request = self.context.get("request")

        user = request.user

        validated_data["user_id"] = user

        budget = Budget.objects.create(**validated_data)
        return budget
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be earlier than start date."}
            )
        return data