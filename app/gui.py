import customtkinter as ctk

from database import criar_tabelas

from telas.login import tela_login
from telas.dashboard import tela_dashboard
from telas.clientes import tela_clientes
from telas.produtos import tela_produtos
from telas.adicionais import tela_adicionais
from telas.pedidos import tela_pedidos
from telas.historico import tela_historico
from telas.fechamento import tela_fechamento
from telas.configuracoes import tela_configuracoes
from telas.usuarios import tela_usuarios
from telas.backup import tela_backup

from theme import (
    COLORS,
    FONTS,
    APP_NAME,
    aplicar_tema
)


# =========================
# TEMA
# =========================
aplicar_tema(ctk)


# =========================
# APP
# =========================
app = ctk.CTk()

app.title(APP_NAME)
app.geometry("1400x800")

app.configure(
    fg_color=COLORS["bg"]
)


# =========================
# BOTÃO MENU
# =========================
def criar_botao(menu, texto, comando):

    ctk.CTkButton(
        menu,
        text=texto,
        command=comando,
        height=48,
        corner_radius=14,
        fg_color=COLORS["primary"],
        hover_color=COLORS["primary_hover"],
        text_color=COLORS["text"],
        font=FONTS["button"],
        anchor="w"
    ).pack(
        fill="x",
        padx=14,
        pady=6
    )


# =========================
# ABRIR SISTEMA
# =========================
def abrir_sistema(usuario_logado):

    for widget in app.winfo_children():
        widget.destroy()

    usuario_nome = usuario_logado[1]
    usuario_tipo = usuario_logado[2]

    # =========================
    # SIDEBAR
    # =========================
    menu = ctk.CTkFrame(
        app,
        width=270,
        fg_color=COLORS["sidebar"],
        corner_radius=0
    )

    menu.pack(
        side="left",
        fill="y"
    )

    # =========================
    # LOGO / TÍTULO
    # =========================
    ctk.CTkLabel(
        menu,
        text=APP_NAME,
        font=("Arial", 30, "bold"),
        text_color=COLORS["text"]
    ).pack(
        pady=(30, 10)
    )

    ctk.CTkLabel(
        menu,
        text=f"Usuário: {usuario_nome}",
        font=FONTS["normal"],
        text_color=COLORS["muted"]
    ).pack()

    ctk.CTkLabel(
        menu,
        text=f"Perfil: {usuario_tipo}",
        font=FONTS["small"],
        text_color=COLORS["muted"]
    ).pack(
        pady=(0, 25)
    )

    # =========================
    # ÁREA CONTEÚDO
    # =========================
    area_conteudo = ctk.CTkFrame(
        app,
        fg_color=COLORS["bg"],
        corner_radius=0
    )

    area_conteudo.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # MENU GERAL
    # =========================
    criar_botao(
        menu,
        "📊 Dashboard",
        lambda: tela_dashboard(area_conteudo)
    )

    criar_botao(
        menu,
        "👥 Clientes",
        lambda: tela_clientes(area_conteudo)
    )

    criar_botao(
        menu,
        "📦 Produtos",
        lambda: tela_produtos(area_conteudo)
    )

    criar_botao(
        menu,
        "➕ Adicionais",
        lambda: tela_adicionais(area_conteudo)
    )

    criar_botao(
        menu,
        "🧾 Pedidos",
        lambda: tela_pedidos(area_conteudo)
    )

    criar_botao(
        menu,
        "📁 Histórico",
        lambda: tela_historico(area_conteudo)
    )

    # =========================
    # ADMIN
    # =========================
    if usuario_tipo == "Administrador":

        criar_botao(
            menu,
            "💰 Fechamento",
            lambda: tela_fechamento(area_conteudo)
        )

        criar_botao(
            menu,
            "⚙ Configurações",
            lambda: tela_configuracoes(area_conteudo)
        )

        criar_botao(
            menu,
            "👤 Usuários",
            lambda: tela_usuarios(area_conteudo)
        )

        criar_botao(
            menu,
            "💾 Backup",
            lambda: tela_backup(area_conteudo)
        )

    # =========================
    # ESPAÇADOR
    # =========================
    espacador = ctk.CTkLabel(
        menu,
        text=""
    )

    espacador.pack(
        expand=True
    )

    # =========================
    # SAIR
    # =========================
    ctk.CTkButton(
        menu,
        text="🚪 Sair",
        command=voltar_login,
        height=48,
        corner_radius=14,
        fg_color=COLORS["danger"],
        hover_color=COLORS["danger_hover"],
        text_color=COLORS["text"],
        font=FONTS["button"]
    ).pack(
        fill="x",
        padx=14,
        pady=20
    )

    # =========================
    # TELA INICIAL
    # =========================
    tela_dashboard(area_conteudo)


# =========================
# LOGIN
# =========================
def voltar_login():

    for widget in app.winfo_children():
        widget.destroy()

    tela_login(
        app,
        abrir_sistema
    )


# =========================
# START
# =========================
criar_tabelas()

tela_login(
    app,
    abrir_sistema
)

app.mainloop()