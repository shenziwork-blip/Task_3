import requests
from uuid import uuid4
from constants import BASE_URL


def create_user():
    email = f"ui_test_{uuid4().hex[:8]}@yandex.ru"
    password = "password123"
    name = "UI Test User"

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
    response.raise_for_status()
    data = response.json()
    token = data.get("accessToken")
    if not token:
        raise ValueError("User registration response did not include accessToken")
    return email, password, token


def delete_user(token):
    if token:
        headers = {"Authorization": token}
        response = requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)
        response.raise_for_status()
        