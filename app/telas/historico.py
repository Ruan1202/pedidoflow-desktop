from services import listar_pedidos, ler_txt_pedido
import customtkinter as ctk


def tela_historico(area_conteudo):
    for widget in area_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        area_conteudo,
        text="Histórico de Pedidos",
        font=("Arial", 24)
    ).pack(pady=10)

    frame_principal = ctk.CTkFrame(area_conteudo)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

    frame_lista = ctk.CTkScrollableFrame(frame_principal, width=420)
    frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_detalhes = ctk.CTkFrame(frame_principal)
    frame_detalhes.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(
        frame_lista,
        text="Pedidos",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=10, pady=5)

    ctk.CTkLabel(
        frame_detalhes,
        text="Detalhes do Pedido",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=10, pady=5)

    texto_detalhes = ctk.CTkTextbox(frame_detalhes)
    texto_detalhes.pack(fill="both", expand=True, padx=10, pady=10)

    mensagem = ctk.CTkLabel(area_conteudo, text="")
    mensagem.pack(pady=5)

    def visualizar_pedido(pedido_id):
        texto = ler_txt_pedido(pedido_id)

        texto_detalhes.delete("1.0", "end")
        texto_detalhes.insert("1.0", texto)

        mensagem.configure(text=f"Pedido #{pedido_id} carregado.")

    pedidos = listar_pedidos()

    if not pedidos:
        ctk.CTkLabel(
            frame_lista,
            text="Nenhum pedido encontrado."
        ).pack(anchor="w", padx=10, pady=5)
        return

    for p in pedidos:
        pedido_id = p[0]
        cliente = p[1]
        total = p[2]
        status = p[3]
        data_hora = p[4]
        observacao = p[5] or ""

        linha = ctk.CTkFrame(frame_lista)
        linha.pack(fill="x", padx=5, pady=5)

        texto = (
            f"#{pedido_id} | {cliente}\n"
            f"Total: R$ {total:.2f} | {status}\n"
            f"{data_hora}"
        )

        if observacao:
            texto += f"\nObs: {observacao}"

        ctk.CTkLabel(
            linha,
            text=texto,
            justify="left"
        ).pack(side="left", padx=10, pady=5)

        ctk.CTkButton(
            linha,
            text="Visualizar",
            width=90,
            command=lambda id_pedido=pedido_id: visualizar_pedido(id_pedido)
        ).pack(side="right", padx=5)