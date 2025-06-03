import requests
import json
import dotenv
import os
dotenv.load_dotenv()
QUOTE_URL = os.getenv("API_KEY_QUOTE")
HISTORY_URL = os.getenv("API_KEY_HISTORY")

def get_stock_data(action_id, period=None):
    with open('data/index.json', 'r', encoding='utf-8') as file:
        index_data = json.load(file)

    stock_code = index_data.get(str(action_id))
    if not stock_code:
        return None

    if period:
        url = HISTORY_URL.format(stock_code=stock_code, period=period)
    else:
        url = QUOTE_URL.format(stock_code=stock_code)

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    
    print("❌ Falha ao buscar dados:", response.status_code, response.text)
    return None
