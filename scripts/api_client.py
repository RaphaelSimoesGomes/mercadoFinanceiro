import os
import json
import requests
from pathlib import Path
import dotenv

dotenv.load_dotenv()

def get_stock_data(action_id):
    base_dir = Path(__file__).parent.parent
    json_path = base_dir / 'data' / 'index.json'
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            index_data = json.load(file)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Formato JSON inválido no arquivo: {json_path}")
        return None
    
    stock_code = index_data.get(str(action_id))
    if not stock_code:
        print(f"Erro: Código de ação não encontrado para o ID: {action_id}")
        return None
    
    url = f"https://brapi.dev/api/quote/{stock_code}"
    
    api_token = os.getenv("BRAPI_TOKEN")
    if api_token:
        url = f"{url}?token={api_token}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP: {e}")
        return None