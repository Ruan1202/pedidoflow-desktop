from services import (
    adicionar_cliente,
    listar_clientes,
    editar_cliente,
    marcar_cliente_lista_negra
)
import customtkinter as ctk


def tela_clientes(area_conteudo):
    for widget in area_conteudo.winfo_children():
        widget.destroy()

    cliente_selecionado = {"id": None}
    lista_negra_var = ctk.IntVar(value=0)

    ctk.CTkLabel(area_conteudo, text="Clientes", font=("Arial", 24)).pack(pady=10)

    frame = ctk.CTkFrame(area_conteudo)
    frame.pack(pady=10)

    nome = ctk.CTkEntry(frame, placeholder_text="Nome")
    nome.pack(pady=5)

    telefone = ctk.CTkEntry(frame, placeholder_text="Telefone")
    telefone.pack(pady=5)

    endereco = ctk.CTkEntry(frame, placeholder_text="Endereço")
    endereco.pack(pady=5)

    bairro = ctk.CTkEntry(frame, placeholder_text="Bairro")
    bairro.pack(pady=5)

    obs = ctk.CTkEntry(frame, placeholder_text="Observações")
    obs.pack(pady=5)

    check_lista_negra = ctk.CTkCheckBox(
        frame,
        text="Cliente problemático / Lista negra",
        variable=lista_negra_var
    )
    check_lista_negra.pack(pady=5)

    mensagem = ctk.CTkLabel(area_conteudo, text="")
    mensagem.pack(pady=5)

    lista = ctk.CTkScrollableFrame(area_conteudo)
    lista.pack(fill="both", expand=True, padx=20, pady=10)

    def limpar_campos():
        cliente_selecionado["id"] = None
        lista_negra_var.set(0)

        nome.delete(0, "end")
        telefone.delete(0, "end")
        endereco.delete(0, "end")
        bairro.delete(0, "end")
        obs.delete(0, "end")

    def selecionar_cliente(cliente):
        cliente_selecionado["id"] = cliente[0]

        nome.delete(0, "end")
        telefone.delete(0, "end")
        endereco.delete(0, "end")
        bairro.delete(0, "end")
        obs.delete(0, "end")

        nome.insert(0, cliente[1] or "")
        telefone.insert(0, cliente[2] or "")
        endereco.insert(0, cliente[3] or "")
        bairro.insert(0, cliente[4] or "")
        obs.insert(0, cliente[5] or "")

        if len(cliente) > 6:
            lista_negra_var.set(cliente[6])
        else:
            lista_negra_var.set(0)

        mensagem.configure(text=f"Cliente #{cliente[0]} selecionado para edição.")

    def atualizar():
        for w in lista.winfo_children():
            w.destroy()

        clientes = listar_clientes()

        if not clientes:
            ctk.CTkLabel(lista, text="Nenhum cliente cadastrado.").pack(anchor="w", padx=10, pady=5)
            return

        for c in clientes:
            linha = ctk.CTkFrame(lista)
            linha.pack(fill="x", padx=5, pady=4)

            status = " ⚠️ LISTA NEGRA" if len(c) > 6 and c[6] == 1 else ""
            texto = f"{c[0]} - {c[1]} | {c[2]} | {c[4]}{status}"

            ctk.CTkLabel(linha, text=texto).pack(side="left", padx=10)

            ctk.CTkButton(
                linha,
                text="Editar",
                width=80,
                command=lambda cliente=c: selecionar_cliente(cliente)
            ).pack(side="right", padx=5)

            if len(c) > 6 and c[6] == 1:
                texto_botao = "Remover alerta"
                novo_status = 0
            else:
                texto_botao = "Lista negra"
                novo_status = 1

            ctk.CTkButton(
                linha,
                text=texto_botao,
                width=110,
                fg_color="#8B0000" if novo_status == 1 else "#2E8B57",
                hover_color="#A00000" if novo_status == 1 else "#3CB371",
                command=lambda cliente_id=c[0], status=novo_status: alternar_lista_negra(cliente_id, status)
            ).pack(side="right", padx=5)

    def salvar():
        mensagem.configure(text="")

        if not nome.get().strip():
            mensagem.configure(text="Informe o nome do cliente.")
            return

        if cliente_selecionado["id"]:
            editar_cliente(
                cliente_selecionado["id"],
                nome.get(),
                telefone.get(),
                endereco.get(),
                bairro.get(),
                obs.get(),
                lista_negra_var.get()
            )
            mensagem.configure(text="Cliente atualizado com sucesso.")
        else:
            adicionar_cliente(
                nome.get(),
                telefone.get(),
                endereco.get(),
                bairro.get(),
                obs.get(),
                lista_negra_var.get()
            )
            mensagem.configure(text="Cliente cadastrado com sucesso.")

        limpar_campos()
        atualizar()

    def alternar_lista_negra(cliente_id, status):
        marcar_cliente_lista_negra(cliente_id, status)
        mensagem.configure(
            text="Status de lista negra atualizado."
        )
        limpar_campos()
        atualizar()

    botoes = ctk.CTkFrame(frame)
    botoes.pack(pady=10)

    ctk.CTkButton(botoes, text="Salvar", command=salvar).pack(side="left", padx=5)
    ctk.CTkButton(botoes, text="Limpar", command=limpar_campos).pack(side="left", padx=5)

    atualizar()