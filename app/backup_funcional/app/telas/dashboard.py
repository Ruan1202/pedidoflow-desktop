import customtkinter as ctk
from services import dados_dashboard


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


def tela_dashboard(area_conteudo):
    for widget in area_conteudo.winfo_children():
        widget.destroy()

    dados = dados_dashboard()

    ctk.CTkLabel(
        area_conteudo,
        text="Dashboard",
        font=("Arial", 28, "bold")
    ).pack(pady=15)

    frame = ctk.CTkFrame(area_conteudo)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    criar_card(frame, "Total vendido", f"R$ {dados['total_vendido']:.2f}")
    criar_card(frame, "Quantidade de pedidos", str(dados["quantidade_pedidos"]))
    criar_card(frame, "Ticket médio", f"R$ {dados['ticket_medio']:.2f}")
    criar_card(frame, "Total em entregas", f"R$ {dados['total_entregas']:.2f}")
    criar_card(frame, "Produto mais vendido", dados["mais_vendido"])
    criar_card(frame, "Clientes cadastrados", str(dados["total_clientes"]))
    criar_card(frame, "Produtos ativos", str(dados["total_produtos"]))