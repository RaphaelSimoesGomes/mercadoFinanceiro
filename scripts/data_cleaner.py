def extract_main_info(api_data):
    results = api_data.get('results', [])
    if results:
        stock = results[0]
        return (
            stock.get('symbol', ''),
            stock.get('longName', ''),
            stock.get('regularMarketPrice', ''),
            stock.get('regularMarketChangePercent', '')
        )
    return ('', '', '', '')
