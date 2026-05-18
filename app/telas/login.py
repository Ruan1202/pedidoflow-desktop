import customtkinter as ctk
from services import validar_login


def tela_login(app, abrir_sistema):

    frame_login = ctk.CTkFrame(app)
    frame_login.pack(expand=True)

    ctk.CTkLabel(
        frame_login,
        text="Bem vindo!!!",
        font=("Arial", 28, "bold")
    ).pack(pady=(20, 10))

    ctk.CTkLabel(
        frame_login,
        text="Login do Sistema",
        font=("Arial", 18)
    ).pack(pady=(0, 20))

    usuario_entry = ctk.CTkEntry(
        frame_login,
        width=250,
        placeholder_text="Usuário"
    )
    usuario_entry.pack(pady=10)

    senha_entry = ctk.CTkEntry(
        frame_login,
        width=250,
        placeholder_text="Senha",
        show="*"
    )
    senha_entry.pack(pady=10)

    mensagem = ctk.CTkLabel(
        frame_login,
        text="",
        text_color="red"
    )
    mensagem.pack(pady=5)

    def fazer_login():

        usuario = usuario_entry.get().strip()
        senha = senha_entry.get().strip()

        if not usuario or not senha:
            mensagem.configure(text="Preencha usuário e senha.")
            return

        usuario_validado = validar_login(usuario, senha)

        if not usuario_validado:
            mensagem.configure(text="Usuário ou senha inválidos.")
            return

        frame_login.destroy()

        abrir_sistema(usuario_validado)

    ctk.CTkButton(
        frame_login,
        text="Entrar",
        width=250,
        command=fazer_login
    ).pack(pady=20)