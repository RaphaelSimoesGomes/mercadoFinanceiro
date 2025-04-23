from scripts.api_client import get_stock_data

action_id = '20'

data = get_stock_data(action_id)

if data:
    results = data.get('results', [])
    if results:
        
        stock = results[0]
        
        nome = stock.get('longName', 'Nome não disponível')
        preco = stock.get('regularMarketPrice', 'Preço não disponível')
        variacao = stock.get('regularMarketChangePercent', 'Variação não disponível')

        resultado = f"Ação: {nome} | Código: {stock.get('symbol', '')} | Preço: R${preco} | Variação: {variacao}%"
        print(resultado)
    else:
        print("Dados da ação não encontrados na resposta da API.")
