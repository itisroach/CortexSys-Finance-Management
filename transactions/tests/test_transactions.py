import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from transactions.models import Transaction
from accounts.models import Account
from utils.helper import get_authoized_client_and_user, get_transaction_data

@pytest.mark.django_db
def test_create_transactions_success():

    _, client = get_authoized_client_and_user()

    data = get_transaction_data()

    response = client.post(reverse("transactions-list"), data, format="json")

    assert response.status_code == 201
    assert data["title"] in str(response.data)


@pytest.mark.django_db
def test_transactions_not_authorized(client: APIClient):
    data = get_transaction_data(True)

    response = client.post(reverse("transactions-list"), data, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_transactions_fail():

    _, client = get_authoized_client_and_user()

    data = get_transaction_data(fail=True)

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

    user, client = get_authoized_client_and_user()

    data = get_transaction_data(user_id=user)

    Transaction.objects.create(**data)

    response = client.get(reverse("transactions-list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_transaction_fail():

    _, client = get_authoized_client_and_user()

    secondUser = Account.objects.create_user(
        phone_number="09140329712", password="something"
    )

    data = get_transaction_data(user_id=secondUser)

    instance = Transaction.objects.create(**data)

    response = client.delete(reverse("transactions-detail", args=[instance.pk]))

    assert response.status_code == 404
    assert "not" in str(response.data)


@pytest.mark.django_db
def test_delete_transaction_not_authorized(client: APIClient):

    response = client.delete(reverse("transactions-detail", args=[1]))

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_transaction_success():

    user, client = get_authoized_client_and_user()

    data = get_transaction_data(user_id=user)

    instance = Transaction.objects.create(**data)

    response = client.delete(reverse("transactions-detail", args=[instance.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update_transaction_not_authorized(client: APIClient):
    response = client.put(reverse("transactions-detail", args=[1]))

    assert response.status_code == 401

    response = client.patch(reverse("transactions-detail", args=[1]))

    assert response.status_code == 401


@pytest.mark.django_db
def test_update_transaction_success():

    user, client = get_authoized_client_and_user()

    data = get_transaction_data(user_id=user)

    instance = Transaction.objects.create(**data)

    del data["user_id"]

    response = client.put(
        reverse("transactions-detail", args=[instance.pk]), data, format="json"
    )

    assert response.status_code == 200
    assert data["title"] in str(response.data)

    response = client.patch(
        reverse("transactions-detail", args=[instance.pk]), {"title": "test2"}
    )

    assert response.status_code == 200
    assert "test2" in str(response.data)
