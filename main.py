import time
from datetime import datetime
from scripts.api_client import get_stock_data
from scripts.get_signal import get_signal
import sys
import random

def main():
    action_id = random.randint(1, 20)
    if len(sys.argv) > 1:
        action_id = sys.argv[1]

    query_interval = 60 
    print(f"Monitorando a ação: {action_id}")
    
    while True:
        try:
            data = get_stock_data(action_id)
            
            if data and 'results' in data and len(data['results']) > 0:
                stock = data['results'][0]
                nome = stock.get('longName', stock.get('symbol', 'Nome não disponível'))
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

if __name__ == "__main__":
    main()