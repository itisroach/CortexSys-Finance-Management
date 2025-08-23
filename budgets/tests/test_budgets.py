import pytest
from rest_framework.test import APIClient
from utils.helper import get_authoized_client_and_user, get_budget_data
from django.urls import reverse
from budgets.models import Budget
from accounts.models import Account


@pytest.mark.django_db
def test_create_budget_success():

    _, client = get_authoized_client_and_user()

    data = get_budget_data()

    response = client.post(reverse("budgets-list"), data, format="json")

    assert response.status_code == 201
    assert data["title"] in str(response.data)


@pytest.mark.django_db
def test_create_budget_fail():
    _, client = get_authoized_client_and_user()

    data = get_budget_data(fail=True)

    response = client.post(reverse("budgets-list"), data, format="json")

    assert response.status_code == 400
    assert "title" in str(response.data)
    assert "total_amount" in str(response.data)
    assert "start_date" in str(response.data)
    assert "end_date" in str(response.data)


@pytest.mark.django_db
def test_create_budget_end_date_earlier_than_start_date():
    _, client = get_authoized_client_and_user()

    data = {
        "title": "sdasa",
        "total_amount": 334,
        "start_date": "2034-3-2",
        "end_date": "2024-1-1",
    }

    response = client.post(reverse("budgets-list"), data, format="json")

    assert response.status_code == 400
    assert "earlier" in str(response.data)


@pytest.mark.django_db
def test_create_budget_not_authorized(client: APIClient):

    response = client.post(reverse("budgets-list"), {}, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_budget():

    user, client = get_authoized_client_and_user()

    data = get_budget_data(user_id=user)

    Budget.objects.create(**data)

    response = client.get(reverse("budgets-list"), format="json")

    assert response.status_code == 200
    assert data["title"] in str(response.data)


@pytest.mark.django_db
def test_get_budget_not_authorized(client: APIClient):

    response = client.get(reverse("budgets-list"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_budget_success():

    user, client = get_authoized_client_and_user()

    data = get_budget_data(user_id=user)

    instance = Budget.objects.create(**data)

    response = client.delete(
        reverse("budgets-detail", args=[instance.pk]), format="json"
    )

    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_budget_fail():

    _, client = get_authoized_client_and_user()

    secondUser = Account.objects.create_user(
        phone_number="09140329712", password="something"
    )

    data = get_budget_data(user_id=secondUser)

    instance = Budget.objects.create(**data)

    response = client.delete(reverse("budgets-detail", args=[instance.pk]))

    assert response.status_code == 404
    assert "not" in str(response.data)


@pytest.mark.django_db
def test_delete_budget_not_authorized(client: APIClient):

    response = client.delete(reverse("budgets-detail", args=[1]))

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_budget_success():

    user, client = get_authoized_client_and_user()

    data = get_budget_data(user_id=user)

    instance = Budget.objects.create(**data)

    response = client.delete(reverse("budgets-detail", args=[instance.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update_budget_not_authorized(client: APIClient):
    response = client.put(reverse("budgets-detail", args=[1]))

    assert response.status_code == 401

    response = client.patch(reverse("budgets-detail", args=[1]))

    assert response.status_code == 401


@pytest.mark.django_db
def test_update_budget_success():

    user, client = get_authoized_client_and_user()

    data = get_budget_data(user_id=user)

    instance = Budget.objects.create(**data)

    del data["user_id"]

    response = client.put(
        reverse("budgets-detail", args=[instance.pk]), data, format="json"
    )

    assert response.status_code == 200
    assert data["title"] in str(response.data)

    response = client.patch(
        reverse("budgets-detail", args=[instance.pk]), {"title": "test"}
    )

    assert response.status_code == 200
    assert "test" in str(response.data)
