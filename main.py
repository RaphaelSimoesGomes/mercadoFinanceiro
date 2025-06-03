from taipy.gui import Gui, notify, get_state_id, invoke_callback
from scripts.api_client import get_stock_data
from scripts.get_signal import get_signal
import json
import pandas as pd
from datetime import datetime
import threading
import time

with open('data/index.json', 'r', encoding='utf-8') as file:
    index_data = json.load(file)

stock_options = list(index_data.values())
id_to_stock = {v: k for k, v in index_data.items()}

selected_stock = "PETR4"
stock_info = {
    "name": "Carregando...",
    "price": None,
    "change": None,
    "signal": "Aguardando dados..."
}
historical_range = "1mo"
period_options = ["1d", "5d", "1mo", "3mo"]
stock_data = pd.DataFrame({
    "Tempo": [],
    "Preço": [],
    "Variação (%)": []
})

auto_refresh = True
refresh_interval = 15
next_update = 10
loading = False
update_thread = None
should_stop = False

def update_stock_data(state):
    state.loading = True
    try:
        ticker = id_to_stock.get(state.selected_stock, state.selected_stock)
        period = state.historical_range

        data   = get_stock_data(ticker, period)
        prices = (data.get("results") or [{}])[0]["historicalDataPrice"]

        if not prices:
            notify(state, "error", "Sem dados históricos.")
            return

        df = (pd.DataFrame(prices)
                .assign(
                    Tempo = lambda d: pd.to_datetime(
                        d["date"].astype("int64"), unit="s", utc=True
                    ).dt.tz_convert("America/Sao_Paulo")
                    .dt.strftime("%d/%m/%Y"),
                    Preço = lambda d: d["close"].astype(float)
                )
                .loc[:, ["Tempo", "Preço"]])

        df["Variação (%)"] = df["Preço"].pct_change().mul(100).fillna(0)

        state.stock_data = df.sort_values("Tempo").reset_index(drop=True)
        last_price, last_pct = df.iloc[-1][["Preço", "Variação (%)"]]

        state.stock_info = {
            "name"  : state.selected_stock,
            "price" : last_price,
            "change": last_pct,
            "signal": get_signal(last_pct)
        }

        notify(state, "success", f"Histórico de {period} carregado.")
    except Exception as err:
        notify(state, "error", f"Erro: {err}")
    finally:
        state.loading = False


def on_period_change(state, var_name, var_value):
    update_stock_data(state)


def on_stock_change(state, var_name, var_value):
    state.stock_data = pd.DataFrame({
        "Tempo": [],
        "Preço": [],
        "Variação (%)": []
    })
    update_stock_data(state)

def auto_update_worker(state_id):
    global should_stop
    while not should_stop:
        if gui and not should_stop:
            invoke_callback(gui, state_id, update_stock_data)
        time.sleep(refresh_interval)

def toggle_auto_refresh(state):
    global update_thread, should_stop
    
    state.auto_refresh = not state.auto_refresh
    
    if state.auto_refresh and (update_thread is None or not update_thread.is_alive()):
        should_stop = False
        update_thread = threading.Thread(target=auto_update_worker, args=[get_state_id(state)])
        update_thread.daemon = True
        update_thread.start()
        msg = "Ativada"
    else:
        should_stop = True
        if update_thread and update_thread.is_alive():
            update_thread.join(timeout=1)
        update_thread = None
        msg = "Desativada"
    
    notify(state, "info", f"Atualização automática {msg}")

def on_interval_change(state, var_name, var_value):
    global refresh_interval
    refresh_interval = state.refresh_interval
    state.next_update = state.refresh_interval

def format_price(price):
    if price is None:
        return "N/A"
    try:
        return f"{float(price):.2f}"
    except Exception:
        return "N/A"

def format_change(change):
    if change is None:
        return "N/A"
    try:
        return f"{float(change):.2f}"
    except Exception:
        return "N/A"

page = """
<|container|
# Dashboard de Ações Brasileiras

<|layout|columns=1 1 1|
<|container|
## Selecione uma Ação
<|{selected_stock}|selector|lov={stock_options}|on_change=on_stock_change|dropdown|>
|>
<|container|
## Configurações
<|{auto_refresh}|toggle|label=Atualização automática|on_change=toggle_auto_refresh|>
<|{refresh_interval}|number|label=Intervalo (s)|min=1|max=60|on_change=on_interval_change|>
<|{historical_range}|selector|label=Período Histórico|lov={period_options}|on_change=on_period_change|dropdown|>
|>
<|container|
## Controles
<|Atualizar Agora|button|on_action=update_stock_data|class_name=primary|>
|>
|>
<|layout|columns=1 2|
<|card|
## <|{stock_info["name"]}|>
**Preço Atual:** R$ <|{format_price(stock_info["price"])}|>
**Variação 24h:** <|{format_change(stock_info["change"])}|>%
**Recomendação:** <|{stock_info["signal"]}|>
|>
<|container|
## Histórico de Preços
<|{stock_data}|table|page_size=10|allow_all_rows=True|show_all=False|striped=True|bordered=True|width=100%|>
|>
|>
<|layout|columns=1|
<|container|
## Gráfico de Evolução de Preço
<|{stock_data}|chart|x=Tempo|y=Preço|type=line|title=Evolução do Preço|height=400px|>

## Gráfico de Variação Percentual
<|{stock_data}|chart|x=Tempo|y=Variação (%)|type=line|title=Variação Percentual|color=blue|height=400px|>
|>
|>
|>
"""

gui = Gui(page)

def on_init(state):
    update_stock_data(state)
    if state.auto_refresh:
        toggle_auto_refresh(state)
if __name__ == "__main__":
    gui.run(title="Stock Dashboard", port=5001, use_reloader=True, on_init=on_init)