import customtkinter as ctk
from tkinter import messagebox

from services import (
    listar_usuarios,
    criar_usuario,
    excluir_usuario
)


def tela_usuarios(area_conteudo):

    for widget in area_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        area_conteudo,
        text="Usuários",
        font=("Arial", 28, "bold")
    ).pack(pady=15)

    frame_topo = ctk.CTkFrame(area_conteudo)
    frame_topo.pack(fill="x", padx=20, pady=10)

    usuario_entry = ctk.CTkEntry(
        frame_topo,
        placeholder_text="Usuário",
        width=200
    )
    usuario_entry.grid(row=0, column=0, padx=10, pady=10)

    senha_entry = ctk.CTkEntry(
        frame_topo,
        placeholder_text="Senha",
        show="*",
        width=200
    )
    senha_entry.grid(row=0, column=1, padx=10, pady=10)

    tipo_option = ctk.CTkOptionMenu(
        frame_topo,
        values=["Administrador", "Atendente"]
    )
    tipo_option.grid(row=0, column=2, padx=10, pady=10)

    lista_frame = ctk.CTkScrollableFrame(area_conteudo)
    lista_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def carregar_usuarios():

        for widget in lista_frame.winfo_children():
            widget.destroy()

        usuarios = listar_usuarios()

        usuarios = [
            u for u in usuarios
            if u[1].lower() != "admin"
        ]
        

        if not usuarios:

            ctk.CTkLabel(
                lista_frame,
                text="Nenhum usuário cadastrado."
            ).pack(pady=10)

            return

        for usuario in usuarios:

            frame_usuario = ctk.CTkFrame(lista_frame)
            frame_usuario.pack(fill="x", pady=5)

            ctk.CTkLabel(
                frame_usuario,
                text=f"{usuario[1]} ({usuario[2]})",
                font=("Arial", 16)
            ).pack(side="left", padx=10, pady=10)

            ctk.CTkButton(
                frame_usuario,
                text="Excluir",
                width=100,
                fg_color="#8B0000",
                hover_color="#A00000",
                command=lambda u=usuario[0]: deletar_usuario(u)
            ).pack(side="right", padx=10)

    def cadastrar_usuario():

        usuario = usuario_entry.get().strip()
        senha = senha_entry.get().strip()
        tipo = tipo_option.get()

        if not usuario or not senha:

            messagebox.showwarning(
                "Aviso",
                "Preencha usuário e senha."
            )

            return

        sucesso, mensagem = criar_usuario(
            usuario,
            senha,
            tipo
        )

        if sucesso:

            messagebox.showinfo(
                "Sucesso",
                mensagem
            )

            usuario_entry.delete(0, "end")
            senha_entry.delete(0, "end")

            carregar_usuarios()

        else:

            messagebox.showerror(
                "Erro",
                mensagem
            )

    def deletar_usuario(usuario_id):

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja realmente excluir este usuário?"
        )

        if not confirmar:
            return

        excluir_usuario(usuario_id)

        carregar_usuarios()

    ctk.CTkButton(
        frame_topo,
        text="Cadastrar",
        command=cadastrar_usuario
    ).grid(row=0, column=3, padx=10, pady=10)

    carregar_usuarios()