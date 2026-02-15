import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser_unique",
        "email": "testunique@example.com",
        "password": "testpassword123",
        "role": "STUDENT"
    }
    response = requests.post(url, json=data)
    print(f"Registration Status: {response.status_code}")
    print(f"Registration Response: {response.json()}")
    return response.status_code == 201

def test_login():
    url = f"{BASE_URL}/auth/login/"
    data = {
        "username": "testuser_unique",
        "password": "testpassword123"
    }
    response = requests.post(url, json=data)
    print(f"Login Status: {response.status_code}")
    tokens = response.json()
    print(f"Login Response: {tokens}")
    return tokens.get('access')

def test_profile_me(token):
    url = f"{BASE_URL}/profile/me/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"Profile Me Status: {response.status_code}")
    print(f"Profile Me Response: {response.json()}")

def test_profile_update(token):
    url = f"{BASE_URL}/profile/update/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "bio": "I am a student at Educlubs.",
        "preferences": {"theme": "dark"}
    }
    response = requests.patch(url, json=data, headers=headers)
    print(f"Profile Update Status: {response.status_code}")
    print(f"Profile Update Response: {response.json()}")

if __name__ == "__main__":
    # Note: Ensure server is running before executing this script
    if test_registration():
        token = test_login()
        if token:
            test_profile_me(token)
            test_profile_update(token)
