from constants import BASE_URL
import requests
from uuid import uuid4



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
    data = response.json()
    return email, password, data.get("accessToken")


def delete_user(token):
    if token:
        headers = {"Authorization": token}
        requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)
        