import customtkinter as ctk
from services import dados_dashboard

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def criar_card(pai, titulo, valor):
    card = ctk.CTkFrame(pai)
    card.pack(fill="x", padx=10, pady=6)

    ctk.CTkLabel(
        card,
        text=titulo,
        font=("Arial", 14)
    ).pack(anchor="w", padx=12, pady=4)

    ctk.CTkLabel(
        card,
        text=valor,
        font=("Arial", 22, "bold")
    ).pack(anchor="w", padx=12, pady=6)


def criar_linha(pai, texto):
    ctk.CTkLabel(
        pai,
        text=texto,
        font=("Arial", 15),
        anchor="w"
    ).pack(fill="x", padx=10, pady=3)


def criar_grafico_pagamentos(pai, dados_pagamento):
    if not dados_pagamento:
        criar_linha(pai, "Nenhum dado para gráfico.")
        return

    nomes = []
    valores = []

    for pagamento, valor in dados_pagamento:
        nomes.append(pagamento or "Não informado")
        valores.append(valor or 0)

    figura = Figure(figsize=(5, 3), dpi=100)
    grafico = figura.add_subplot(111)

    grafico.bar(nomes, valores)
    grafico.set_title("Vendas por pagamento")
    grafico.set_ylabel("Valor R$")
    grafico.tick_params(axis="x", rotation=20)

    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=pai)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


def tela_dashboard(area_conteudo):
    for widget in area_conteudo.winfo_children():
        widget.destroy()

    dados = dados_dashboard()

    ctk.CTkLabel(
        area_conteudo,
        text="Dashboard",
        font=("Arial", 28, "bold")
    ).pack(pady=15)

    frame_principal = ctk.CTkFrame(area_conteudo)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

    frame_esquerda = ctk.CTkScrollableFrame(frame_principal)
    frame_esquerda.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_direita = ctk.CTkScrollableFrame(frame_principal)
    frame_direita.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    criar_card(frame_esquerda, "Total vendido", f"R$ {dados['total_vendido']:.2f}")
    criar_card(frame_esquerda, "Quantidade de pedidos", str(dados["quantidade_pedidos"]))
    criar_card(frame_esquerda, "Ticket médio", f"R$ {dados['ticket_medio']:.2f}")
    criar_card(frame_esquerda, "Total em entregas", f"R$ {dados['total_entregas']:.2f}")
    criar_card(frame_esquerda, "Produto mais vendido", dados["mais_vendido"])
    criar_card(frame_esquerda, "Clientes cadastrados", str(dados["total_clientes"]))
    criar_card(frame_esquerda, "Produtos ativos", str(dados["total_produtos"]))

    ctk.CTkLabel(
        frame_direita,
        text="Gráfico de pagamentos",
        font=("Arial", 20, "bold")
    ).pack(pady=8)

    criar_grafico_pagamentos(frame_direita, dados["por_pagamento"])

    ctk.CTkLabel(
        frame_direita,
        text="Vendas por pagamento",
        font=("Arial", 20, "bold")
    ).pack(pady=8)

    if dados["por_pagamento"]:
        for pagamento, valor in dados["por_pagamento"]:
            pagamento = pagamento or "Não informado"
            criar_linha(frame_direita, f"{pagamento}: R$ {valor:.2f}")
    else:
        criar_linha(frame_direita, "Nenhum pagamento registrado.")

    ctk.CTkLabel(
        frame_direita,
        text="Últimos pedidos",
        font=("Arial", 20, "bold")
    ).pack(pady=12)

    if dados["ultimos_pedidos"]:
        for pedido in dados["ultimos_pedidos"]:
            pedido_id, cliente, total, pagamento = pedido
            pagamento = pagamento or "Não informado"
            criar_linha(
                frame_direita,
                f"#{pedido_id} | {cliente} | R$ {total:.2f} | {pagamento}"
            )
    else:
        criar_linha(frame_direita, "Nenhum pedido registrado.")

    ctk.CTkLabel(
        frame_direita,
        text="Ranking de produtos",
        font=("Arial", 20, "bold")
    ).pack(pady=12)

    if dados["ranking_produtos"]:
        for produto, quantidade in dados["ranking_produtos"]:
            criar_linha(frame_direita, f"{produto}: {quantidade} vendidos")
    else:
        criar_linha(frame_direita, "Nenhum produto vendido ainda.")