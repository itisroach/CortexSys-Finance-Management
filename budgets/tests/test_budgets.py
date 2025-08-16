import pytest
from rest_framework.test import APIClient
from transactions.tests.test_transactions import get_user_and_token 
from django.urls import reverse
from budgets.models import Budget
from accounts.models import Account


@pytest.mark.django_db
def test_create_budget_success():

    _, token = get_user_and_token()

    data = {
        "title": "test",
        "total_amount": 10000,
        "start_date": "2024-2-4",
        "end_date": "2024-3-4",
    }

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("budgets-list"), data, format="json")


    assert response.status_code == 201
    assert data["title"] in str(response.data)



@pytest.mark.django_db
def test_create_budget_fail():
    _, token = get_user_and_token()

    data = {
        "title": "",
        "total_amount": 0,
        "start_date": "",
        "end_date": "",
    }

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(reverse("budgets-list"), data, format="json")


    assert response.status_code == 400
    assert "title" in str(response.data)
    assert "total_amount" in str(response.data)
    assert "start_date" in str(response.data)
    assert "end_date" in str(response.data)


@pytest.mark.django_db
def test_budget_exceeded():
    _, token = get_user_and_token()

    data = {
        "title": "test title",
        "total_amount": 100,
        "start_date": "2024-5-2",
        "end_date": "2025-5-2",
    }

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    client.post(reverse("budgets-list"), data, format="json")

    trans_data = {
        "title": "test trans",
        "amount": 200,
        "date": "2024-7-2",
        "type": "expense"
    }

    response = client.post(reverse("transactions-list"), trans_data)
    
    assert response.status_code == 403
    assert "exceeded" in str(response.data)


@pytest.mark.django_db
def test_create_budget_not_authorized(client: APIClient):

    response = client.post(reverse("budgets-list"), {}, format="json")

    assert response.status_code == 401



@pytest.mark.django_db
def test_get_budget():

    user, token = get_user_and_token()

    data = {
        "title": "test",
        "total_amount": 10000,
        "start_date": "2024-2-4",
        "end_date": "2024-3-4",
        "user_id": user
    }

    Budget.objects.create(**data)

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(reverse("budgets-list"), format="json")


    assert response.status_code == 200
    assert data["title"] in str(response.data)

@pytest.mark.django_db
def test_get_budget_not_authorized(client: APIClient):

    response = client.get(reverse("budgets-list"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_budget_success():

    user, token = get_user_and_token()

    data = {
        "title": "test",
        "total_amount": 10000,
        "start_date": "2024-2-4",
        "end_date": "2024-3-4",
        "user_id": user
    }

    instance = Budget.objects.create(**data)

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.delete(reverse("budgets-detail", args=[instance.pk]), format="json")


    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_budget_fail():

    _, token = get_user_and_token()

    secondUser = Account.objects.create_user(phone_number="09140329712", password="something")

    data = {
        "title": "test",
        "total_amount": 1000000,
        "start_date": "2024-12-20",
        "end_date": "2024-12-22",
        "user_id": secondUser
    }

    instance = Budget.objects.create(**data)

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.delete(reverse("budgets-detail", args=[instance.pk]))

    assert response.status_code == 404
    assert "not" in str(response.data)


@pytest.mark.django_db
def test_delete_budget_not_authorized(client: APIClient):

    response = client.delete(reverse("budgets-detail", args=[1]))

    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_budget_success():

    user, token = get_user_and_token()

    data = {
        "title": "test",
        "total_amount": 1000000,
        "start_date": "2024-12-20",
        "end_date": "2024-12-22",
        "user_id": user
    }

    instance = Budget.objects.create(**data)

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

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
    
    user, token = get_user_and_token()

    data = {
        "title": "test",
        "total_amount": 1000000,
        "start_date": "2024-12-20",
        "end_date": "2024-12-22",
        "user_id": user
    }
    

    instance = Budget.objects.create(**data)

    del data["user_id"]

    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.put(reverse("budgets-detail", args=[instance.pk]), data, format="json")

    assert response.status_code == 200
    assert data["title"] in str(response.data)


    response = client.patch(reverse("budgets-detail", args=[instance.pk]), {"title": "test"})

    assert response.status_code == 200
    assert "test" in str(response.data)