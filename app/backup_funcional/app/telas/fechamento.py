import customtkinter as ctk
from services import fechamento_do_dia


def criar_card(pai, titulo, valor):
    card = ctk.CTkFrame(pai)
    card.pack(fill="x", padx=15, pady=8)

    ctk.CTkLabel(
        card,
        text=titulo,
        font=("Arial", 15)
    ).pack(anchor="w", padx=15, pady=5)

    ctk.CTkLabel(
        card,
        text=valor,
        font=("Arial", 24, "bold")
    ).pack(anchor="w", padx=15, pady=8)


def tela_fechamento(area_conteudo):

    for widget in area_conteudo.winfo_children():
        widget.destroy()

    dados = fechamento_do_dia()

    total_vendido = dados["total_vendido"]
    total_pedidos = dados["total_pedidos"]
    total_entrega = dados["total_entrega"]
    cancelados = dados["cancelados"]
    mais_vendido = dados["mais_vendido"]

    ticket_medio = 0

    if total_pedidos > 0:
        ticket_medio = total_vendido / total_pedidos

    pagamentos = {
        "PIX": 0,
        "Dinheiro": 0,
        "Débito": 0,
        "Crédito": 0
    }

    for pagamento in dados["por_pagamento"]:
        nome = pagamento[0]
        valor = pagamento[1]

        if nome in pagamentos:
            pagamentos[nome] = valor

    ctk.CTkLabel(
        area_conteudo,
        text="Fechamento Financeiro",
        font=("Arial", 28, "bold")
    ).pack(pady=15)

    frame = ctk.CTkScrollableFrame(area_conteudo)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    criar_card(
        frame,
        "Total vendido",
        f"R$ {total_vendido:.2f}"
    )

    criar_card(
        frame,
        "Quantidade pedidos",
        str(total_pedidos)
    )

    criar_card(
        frame,
        "Ticket médio",
        f"R$ {ticket_medio:.2f}"
    )

    criar_card(
        frame,
        "Total entregas",
        f"R$ {total_entrega:.2f}"
    )

    criar_card(
        frame,
        "Pedidos cancelados",
        str(cancelados)
    )

    criar_card(
        frame,
        "Mais vendido",
        mais_vendido
    )

    criar_card(
        frame,
        "PIX",
        f"R$ {pagamentos['PIX']:.2f}"
    )

    criar_card(
        frame,
        "Dinheiro",
        f"R$ {pagamentos['Dinheiro']:.2f}"
    )

    criar_card(
        frame,
        "Débito",
        f"R$ {pagamentos['Débito']:.2f}"
    )

    criar_card(
        frame,
        "Crédito",
        f"R$ {pagamentos['Crédito']:.2f}"
    )