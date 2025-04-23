import requests
import json

def get_stock_data(action_id):
    with open('data/index.json', 'r', encoding='utf-8') as file:
        index_data = json.load(file)
    stock_code = index_data.get(str(action_id))
    url = f"https://brapi.dev/api/quote/{stock_code}?token=s9ov6rCGRmAyjDeJD1Sq3Q"
    response = requests.get(url)

    if not stock_code:
        return None
    
    if response.status_code == 200:
        return response.json()
    return None
