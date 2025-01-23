import requests

def fetch_historical_quiz_data(api_url):
    """Fetch historical quiz data from the API endpoint."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch historical quiz data: {response.status_code}")

def fetch_current_quiz_data(api_url):
    """Fetch current quiz data from the API endpoint."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch current quiz data: {response.status_code}")
