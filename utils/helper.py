from accounts.models import Account
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient


def get_authoized_client_and_user():
    user = Account.objects.create_user(phone_number="09140329711", password="something")

    accessToken = str(RefreshToken.for_user(user).access_token)

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {accessToken}")

    return user, client


def get_transaction_data(fail: bool = False, user_id=None):
    if not fail:
        return {
            "title": "test",
            "amount": 1000000,
            "type": "income",
            "date": "2024-12-20",
            "notes": "",
            "user_id": user_id or None,
        }
    else:
        return {
            "title": "",
            "amount": 0,
            "type": "",
            "date": "",
            "notes": "",
        }


def get_budget_data(fail: bool = False, user_id=None):
    if not fail:
        return {
            "title": "test",
            "total_amount": 10000,
            "start_date": "2024-2-4",
            "end_date": "2024-3-4",
            "user_id": user_id,
        }
    else:
        return {
            "title": "",
            "total_amount": "",
            "start_date": "",
            "end_date": "",
        }
