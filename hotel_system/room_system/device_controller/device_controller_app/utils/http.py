import requests

def put_http_data(url, payload):
    try:
        response = requests.put(url, json=payload, timeout=5)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Return the response data as JSON
    except requests.exceptions.RequestException as e:
        # Handle errors
        return {'error': str(e)}
