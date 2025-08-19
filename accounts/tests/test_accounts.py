import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import Account, DeviceToken
from transactions.tests.test_transactions import get_user_and_token


@pytest.mark.django_db
def test_create_account_success(client: APIClient):

    data = {"phone_number": "+989140329711", "password": "amirali3362"}

    response = client.post(reverse("register-user"), data, format="json")

    assert response.status_code == 201
    assert "id" in str(response.data)


@pytest.mark.django_db
def test_create_account_failed(client: APIClient):

    # unique phone number

    Account.objects.create_user(phone_number="09140329711", password="something")

    data = {"phone_number": "+989140329711", "password": "amirali3362"}

    response = client.post(reverse("register-user"), data, format="json")
    print("fuck", response)
    assert response.status_code == 400
    assert "exists" in str(response.data)

    # phone number required
    data = {"phone_number": "", "password": "amirali3362"}

    response = client.post(reverse("register-user"), data, format="json")

    assert response.status_code == 400
    assert "blank" in str(response.data)

    # password required
    data = {"phone_number": "+989140329711", "password": ""}

    response = client.post(reverse("register-user"), data, format="json")

    assert response.status_code == 400
    assert "blank" in str(response.data)


@pytest.mark.django_db
def test_login_account_success(client: APIClient):

    Account.objects.create_user(phone_number="09140329711", password="amirali3362")

    data = {"phone_number": "+989140329711", "password": "amirali3362"}

    response = client.post(reverse("login-user"), data, format="json")

    assert response.status_code == 200
    assert "access" in str(response.data)


@pytest.mark.django_db
def test_login_account_failed(client: APIClient):

    # phone number required
    data = {"phone_number": "", "password": "amirali3362"}

    response = client.post(reverse("login-user"), data, format="json")

    assert response.status_code == 400
    assert "blank" in str(response.data)

    # password required
    data = {"phone_number": "+989140329711", "password": ""}

    response = client.post(reverse("login-user"), data, format="json")

    assert response.status_code == 400
    assert "blank" in str(response.data)

    # wrong password

    Account.objects.create_user(phone_number="09140329711", password="something")

    data = {"phone_number": "+989140329711", "password": "wrongpassword"}

    response = client.post(reverse("login-user"), data, format="json")

    assert response.status_code == 401
    assert "found" in str(response.data)


@pytest.mark.django_db
def test_device_token():

    _, token = get_user_and_token()

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {"token": "fake_tokens"}

    response = client.post(reverse("device-token-list"), data=data, format="json")

    assert response.status_code == 201
    assert "fake_tokens" in str(response.data)


@pytest.mark.django_db
def test_device_token_not_authorized():

    client = APIClient()

    data = {"token": "fake_tokens"}

    response = client.post(reverse("device-token-list"), data=data, format="json")

    assert response.status_code == 401
