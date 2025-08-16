import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from transactions.models import Transaction
from accounts.models import Account
from rest_framework_simplejwt.tokens import RefreshToken

def get_user_and_token():
    user = Account.objects.create_user(phone_number="09140329711", password="something")

    accessToken = str(RefreshToken.for_user(user).access_token)

    return user, accessToken

@pytest.mark.django_db
def test_create_transactions_success():

    user, accessToken = get_user_and_token()

    data = {
        "title": "test",
        "amount": 1000000,
        "type": "income",
        "date": "2024-12-20",
        "notes": "",
        "user_id": user.pk
    }

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {accessToken}")

    response = client.post(reverse("transactions-list"), data, format="json")


    assert response.status_code == 201
    assert data["title"] in str(response.data)


@pytest.mark.django_db
def test_transactions_not_authorized(client: APIClient):
    data = {
        "title": "",
        "amount": 0,
        "type": "",
        "date": "",
        "notes": "",
    }

    response = client.post(reverse("transactions-list"), data, format="json")

    assert response.status_code == 401
    

@pytest.mark.django_db
def test_create_transactions_fail():

    user, accessToken = get_user_and_token()

    data = {
        "title": "",
        "amount": 0,
        "type": "",
        "date": "",
        "notes": "",
    }

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {accessToken}")

    response = client.post(reverse("transactions-list"), data, format="json")

    assert response.status_code == 400
    assert "title" in str(response.data)
    assert "type" in str(response.data)
    assert "amount" in str(response.data)
    assert "date" in str(response.data)



@pytest.mark.django_db
def test_get_transactions_not_authorized(client: APIClient):

    response = client.get(reverse("transactions-list"))

    assert response.status_code == 401

@pytest.mark.django_db
def test_get_transactions():

    user, token = get_user_and_token()

    data = {
        "title": "test",
        "amount": 1000000,
        "type": "income",
        "date": "2024-12-20",
        "notes": "",
        "user_id": user
    }

    Transaction.objects.create(**data)


    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(reverse("transactions-list"))

    assert response.status_code == 200