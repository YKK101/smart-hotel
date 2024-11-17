import requests

def get_http_data(url):
    try:
        # Make the GET request
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Return the response data as JSON
    except requests.exceptions.RequestException as e:
        # Handle errors
        return {'error': str(e)}