import requests
import json
import dotenv
import os

dotenv.load_dotenv()
Token = os.getenv("API_KEY");

def get_stock_data(action_id):
    with open('data/index.json', 'r', encoding='utf-8') as file:
        index_data = json.load(file)
    stock_code = index_data.get(str(action_id))
    url = Token.format(stock_code=stock_code)
    response = requests.get(url)

    if not stock_code:
        return None
    
    if response.status_code == 200:
        return response.json()
    return None
