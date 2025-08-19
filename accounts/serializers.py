from rest_framework import serializers
from .models import Account, DeviceToken


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ["id", "phone_number", "password"]

    def create(self, validated_data):
        user = Account.objects.create_user(
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return user


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["id", "token"]
