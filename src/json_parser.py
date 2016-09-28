import requests

def json_parser(response):
    try:
        json_response = response.json()
        
        return json_response
    except ValueError:
        return False