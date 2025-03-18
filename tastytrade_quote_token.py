import requests

def get_quote_token(session_token):
    url = "https://api.tastytrade.com/api-quote-tokens"
    headers = {
        "Authorization": f"Bearer {session_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            quote_token = response.json()["data"]["token"]
            print("Quote token retrieved successfully!")
            return quote_token
        else:
            print("Failed to get quote token:", response.json())
            return None
    except Exception as e:
        print(f"Error getting quote token: {e}")
        return None

if __name__ == "__main__":
    # Replace with your session token
    SESSION_TOKEN = "gP0Z92I8P2-IcCOe6_lZhZqPue672jRH0lx1hM5rYxYPajynWtKMGg+C"
    
    quote_token = get_quote_token(SESSION_TOKEN)
    if quote_token:
        print("Quote token:", quote_token)