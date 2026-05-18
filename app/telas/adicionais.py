import customtkinter as ctk

from services import (
    adicionar_adicional,
    listar_adicionais,
    editar_adicional,
    inativar_adicional
)


def tela_adicionais(area_conteudo):

    for widget in area_conteudo.winfo_children():
        widget.destroy()

    adicional_editando = {
        "id": None
    }

    ctk.CTkLabel(
        area_conteudo,
        text="Adicionais",
        font=("Arial", 24, "bold")
    ).pack(pady=10)

    # =========================
    # FORMULÁRIO
    # =========================
    frame_form = ctk.CTkFrame(area_conteudo)
    frame_form.pack(fill="x", padx=20, pady=10)

    nome = ctk.CTkEntry(
        frame_form,
        placeholder_text="Nome do adicional"
    )
    nome.pack(fill="x", padx=10, pady=5)

    valor = ctk.CTkEntry(
        frame_form,
        placeholder_text="Valor"
    )
    valor.pack(fill="x", padx=10, pady=5)

    mensagem = ctk.CTkLabel(
        area_conteudo,
        text=""
    )
    mensagem.pack(pady=5)

    # =========================
    # LISTA
    # =========================
    lista_frame = ctk.CTkScrollableFrame(
        area_conteudo
    )

    lista_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # =========================
    # FUNÇÕES
    # =========================
    def limpar_campos():
        nome.delete(0, "end")
        valor.delete(0, "end")

        adicional_editando["id"] = None

    def carregar_adicionais():

        for widget in lista_frame.winfo_children():
            widget.destroy()

        adicionais = listar_adicionais()

        if not adicionais:

            ctk.CTkLabel(
                lista_frame,
                text="Nenhum adicional cadastrado."
            ).pack(pady=10)

            return

        for adicional in adicionais:

            frame_item = ctk.CTkFrame(lista_frame)
            frame_item.pack(
                fill="x",
                padx=5,
                pady=5
            )

            texto = (
                f"{adicional[1]} "
                f"- R$ {adicional[2]:.2f}"
            )

            ctk.CTkLabel(
                frame_item,
                text=texto,
                font=("Arial", 16)
            ).pack(
                side="left",
                padx=10
            )

            ctk.CTkButton(
                frame_item,
                text="Editar",
                width=80,
                command=lambda a=adicional: carregar_edicao(a)
            ).pack(
                side="right",
                padx=5,
                pady=5
            )

            ctk.CTkButton(
                frame_item,
                text="Excluir",
                width=80,
                fg_color="#8B0000",
                hover_color="#A00000",
                command=lambda id_adicional=adicional[0]: excluir_adicional(id_adicional)
            ).pack(
                side="right",
                padx=5,
                pady=5
            )

    def salvar_adicional():

        nome_adicional = nome.get().strip()
        valor_adicional = valor.get().strip()

        if not nome_adicional or not valor_adicional:

            mensagem.configure(
                text="Preencha todos os campos."
            )

            return

        try:
            valor_float = float(
                valor_adicional.replace(",", ".")
            )

        except:

            mensagem.configure(
                text="Valor inválido."
            )

            return

        if adicional_editando["id"] is None:

            adicionar_adicional(
                nome_adicional,
                valor_float
            )

            mensagem.configure(
                text="Adicional cadastrado."
            )

        else:

            editar_adicional(
                adicional_editando["id"],
                nome_adicional,
                valor_float
            )

            mensagem.configure(
                text="Adicional atualizado."
            )

        limpar_campos()
        carregar_adicionais()

    def carregar_edicao(adicional):

        adicional_editando["id"] = adicional[0]

        nome.delete(0, "end")
        valor.delete(0, "end")

        nome.insert(0, adicional[1])
        valor.insert(0, str(adicional[2]))

        mensagem.configure(
            text="Modo edição ativado."
        )

    def excluir_adicional(adicional_id):

        inativar_adicional(adicional_id)

        mensagem.configure(
            text="Adicional removido."
        )

        carregar_adicionais()

    # =========================
    # BOTÕES
    # =========================
    frame_botoes = ctk.CTkFrame(frame_form)
    frame_botoes.pack(pady=10)

    ctk.CTkButton(
        frame_botoes,
        text="Salvar",
        command=salvar_adicional
    ).pack(
        side="left",
        padx=5
    )

    ctk.CTkButton(
        frame_botoes,
        text="Limpar",
        command=limpar_campos
    ).pack(
        side="left",
        padx=5
    )

    carregar_adicionais()