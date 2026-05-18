import customtkinter as ctk
from tkinter import filedialog
from helpers.backup import gerar_backup_banco, restaurar_backup_banco


def tela_backup(area_conteudo):
    for widget in area_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        area_conteudo,
        text="Backup do Sistema",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    resultado = ctk.CTkTextbox(area_conteudo, width=750, height=220)
    resultado.pack(pady=20)

    def mostrar_resultado(msg):
        resultado.delete("1.0", "end")
        resultado.insert("1.0", msg)

    def fazer_backup():
        sucesso, msg = gerar_backup_banco()
        mostrar_resultado(msg)

    def restaurar_backup():
        caminho = filedialog.askopenfilename(
            title="Selecione o backup",
            filetypes=[("Banco SQLite", "*.db")]
        )

        sucesso, msg = restaurar_backup_banco(caminho)
        mostrar_resultado(msg)

    ctk.CTkButton(
        area_conteudo,
        text="Gerar Backup",
        width=240,
        height=45,
        command=fazer_backup
    ).pack(pady=10)

    ctk.CTkButton(
        area_conteudo,
        text="Restaurar Backup",
        width=240,
        height=45,
        fg_color="#8B0000",
        hover_color="#A00000",
        command=restaurar_backup
    ).pack(pady=10)