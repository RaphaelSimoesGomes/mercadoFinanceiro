from scripts.api_client import get_stock_data
import time
from datetime import datetime
from scripts.get_signal import get_signal

action_id = '20'
query_interval = 60 

while True:
    try:
        data = get_stock_data(action_id)
        
        if data and 'results' in data and len(data['results']) > 0:
            stock = data['results'][0]
            nome = stock.get('longName', 'Nome não disponível')
            preco = stock.get('regularMarketPrice', 0)
            variacao = stock.get('regularMarketChangePercent', 0)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n[{timestamp}] Ação: {nome}")
            print(f"Preço atual: R${preco:.2f}")
            print(f"Variação: {variacao:.2f}%")
            print(f"Recomendação: {get_signal(variacao)}")
        else:
            print("⚠️ Dados não recebidos da API")
        
    except Exception as e:
        print(f"Erro na consulta: {str(e)}")
    
    print("\n" + "-"*50 + "\nAguardando próxima verificação...")
    time.sleep(query_interval)
