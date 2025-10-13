import requests


def make_request(url, headers=None, timeout=10):
    """Helper function to make HTTP GET requests with error handling."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

