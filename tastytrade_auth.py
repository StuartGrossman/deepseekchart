import requests

def authenticate_tastytrade(username, password):
    url = "https://api.tastytrade.com/sessions"
    payload = {
        "login": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            session_token = response.json()["data"]["token"]
            print("Authentication successful!")
            return session_token
        else:
            print("Authentication failed:", response.json())
            return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

if __name__ == "__main__":
    # Replace with your credentials
    USERNAME = "grossman.stuart1@gmail.com"
    PASSWORD = "Alenviper123"
    
    session_token = authenticate_tastytrade(USERNAME, PASSWORD)
    if session_token:
        print("Session token:", session_token)