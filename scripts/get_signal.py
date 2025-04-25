def get_signal(variacao):
    if variacao <= -2:
        return "COMPRA 🔼 (Queda significativa)"
    elif variacao >= 2:
        return "VENDA 🔽 (Alta expressiva)"
    else:
        return "MANTER ↔️ (Mercado estável)"

print("Iniciando monitoramento de ações...\n")