import customtkinter as ctk

from telas.dashboard import tela_dashboard
from telas.clientes import tela_clientes
from telas.produtos import tela_produtos
from telas.adicionais import tela_adicionais
from telas.pedidos import tela_pedidos
from telas.historico import tela_historico
from telas.fechamento import tela_fechamento
from telas.configuracoes import tela_configuracoes


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("CRM Atendimento")
app.geometry("1200x700")


menu = ctk.CTkFrame(app, width=220)
menu.pack(side="left", fill="y")

titulo = ctk.CTkLabel(
    menu,
    text="CRM Atendimento",
    font=("Arial", 22, "bold")
)
titulo.pack(pady=20)


area_conteudo = ctk.CTkFrame(app)
area_conteudo.pack(side="right", fill="both", expand=True)


ctk.CTkButton(
    menu,
    text="Dashboard",
    height=40,
    command=lambda: tela_dashboard(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Clientes",
    height=40,
    command=lambda: tela_clientes(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Produtos",
    height=40,
    command=lambda: tela_produtos(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Adicionais",
    height=40,
    command=lambda: tela_adicionais(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Pedidos",
    height=40,
    command=lambda: tela_pedidos(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Histórico",
    height=40,
    command=lambda: tela_historico(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Fechamento",
    height=40,
    command=lambda: tela_fechamento(area_conteudo)
).pack(fill="x", padx=15, pady=5)

ctk.CTkButton(
    menu,
    text="Configurações",
    height=40,
    command=lambda: tela_configuracoes(area_conteudo)
).pack(fill="x", padx=15, pady=5)


tela_dashboard(area_conteudo)

app.mainloop()