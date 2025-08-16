import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_create_account_success(client: APIClient):
    
    data = {"phone_number": "09140329711", "password": "amirali3362"}

    response = client.post(reverse('register-user'), data, format="json")

    assert response.status_code == 201
    assert "id" in response.data


@pytest.mark.django_db
def test_create_account_failed(client: APIClient):
    
    # unique phone number
    data = {"phone_number": "09140329711", "password": "amirali3362"}

    response = client.post(reverse('register-user'), data, format="json")

    assert response.status_code == 400
    assert "exists" in response.data

    # phone number required
    data = {"phone_number": "", "password": "amirali3362"}

    response = client.post(reverse('register-user'), data, format="json")

    assert response.status_code == 400
    assert "required" in response.data


    # password required
    data = {"phone_number": "09140329711", "password": ""}

    response = client.post(reverse('register-user'), data, format="json")

    assert response.status_code == 400
    assert "required" in response.data



@pytest.mark.django_db
def test_login_account_success(client: APIClient):

    data = {"phone_number": "09140329711", "password": "amirali3362"}

    response = client.post(reverse("login-user"), data, format="json")

    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_login_account_failed(client: APIClient):
    

    # phone number required
    data = {"phone_number": "", "password": "amirali3362"}

    response = client.post(reverse('login-user'), data, format="json")

    assert response.status_code == 400
    assert "required" in response.data


    # password required
    data = {"phone_number": "09140329711", "password": ""}

    response = client.post(reverse('login-user'), data, format="json")

    assert response.status_code == 400
    assert "required" in response.data


    # wrong password
    data = {"phone_number": "09140329711", "password": "wrongpassword"}

    response = client.post(reverse('login-user'), data, format="json")

    assert response.status_code == 400
    assert "wrong" in response.data

