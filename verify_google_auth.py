import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_missing_token():
    print("Testing missing id_token...")
    try:
        response = requests.post(f"{BASE_URL}/auth/google/", json={})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
        print("Missing token test passed.\n")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Is it running?")

def test_invalid_token():
    print("Testing invalid id_token...")
    try:
        response = requests.post(f"{BASE_URL}/auth/google/", json={"id_token": "invalid.token.here"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
        print("Invalid token test passed.\n")
    except requests.exceptions.ConnectionError:
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # User provided an actual token to test
        token = sys.argv[1]
        print("Testing with provided token...")
        response = requests.post(f"{BASE_URL}/auth/google/", json={"id_token": token})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            print("Successfully authenticated with Google OAuth!")
            token_data = response.json()
            
            # Now try to access profile
            print("\nTesting profile access with new access token...")
            headers = {"Authorization": f"Bearer {token_data['access']}"}
            prof_resp = requests.get(f"{BASE_URL}/profile/me/", headers=headers)
            print(f"Profile Status: {prof_resp.status_code}")
            print(f"Profile Response: {prof_resp.json()}")
            
    else:
        print("Running automated error handling tests...")
        test_missing_token()
        test_invalid_token()
        print("To test a real Google ID Token, run: python verify_google_auth.py <your_id_token>")
