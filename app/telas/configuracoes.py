import customtkinter as ctk
from database import conectar
from theme import salvar_tema, carregar_tema


def tela_configuracoes(area_conteudo):

    for widget in area_conteudo.winfo_children():
        widget.destroy()

    tema_atual = carregar_tema()

    ctk.CTkLabel(
        area_conteudo,
        text="Configurações",
        font=("Arial", 28, "bold")
    ).pack(pady=15)

    abas = ctk.CTkTabview(area_conteudo)
    abas.pack(fill="both", expand=True, padx=20, pady=10)

    aba_loja = abas.add("Loja")
    aba_taxas = abas.add("Taxas")
    aba_aparencia = abas.add("Aparência")

    mensagem = ctk.CTkLabel(area_conteudo, text="")
    mensagem.pack(pady=5)

    # =========================
    # ABA LOJA
    # =========================
    nome_loja = ctk.CTkEntry(
        aba_loja,
        placeholder_text="Nome da loja"
    )
    nome_loja.pack(fill="x", padx=20, pady=8)

    endereco_loja = ctk.CTkEntry(
        aba_loja,
        placeholder_text="Endereço da loja"
    )
    endereco_loja.pack(fill="x", padx=20, pady=8)

    latitude = ctk.CTkEntry(
        aba_loja,
        placeholder_text="Latitude"
    )
    latitude.pack(fill="x", padx=20, pady=8)

    longitude = ctk.CTkEntry(
        aba_loja,
        placeholder_text="Longitude"
    )
    longitude.pack(fill="x", padx=20, pady=8)

    def carregar_configuracoes_loja():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nome_loja, endereco_loja, latitude, longitude
            FROM configuracoes_loja
            LIMIT 1
        """)

        dados = cursor.fetchone()

        conn.close()

        if dados:

            nome_loja.insert(0, dados[0] or "")
            endereco_loja.insert(0, dados[1] or "")
            latitude.insert(0, str(dados[2] or ""))
            longitude.insert(0, str(dados[3] or ""))

    def salvar_configuracoes_loja():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM configuracoes_loja")

        cursor.execute("""
            INSERT INTO configuracoes_loja
            (nome_loja, endereco_loja, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, (
            nome_loja.get(),
            endereco_loja.get(),
            latitude.get(),
            longitude.get()
        ))

        conn.commit()
        conn.close()

        mensagem.configure(
            text="Configurações da loja salvas."
        )

    ctk.CTkButton(
        aba_loja,
        text="Salvar Loja",
        command=salvar_configuracoes_loja
    ).pack(pady=15)

    # =========================
    # ABA TAXAS
    # =========================
    lista_taxas = ctk.CTkScrollableFrame(aba_taxas)
    lista_taxas.pack(fill="both", expand=True, padx=20, pady=10)

    frame_nova_taxa = ctk.CTkFrame(aba_taxas)
    frame_nova_taxa.pack(fill="x", padx=20, pady=10)

    distancia = ctk.CTkEntry(
        frame_nova_taxa,
        placeholder_text="Distância KM"
    )
    distancia.pack(side="left", padx=5, pady=5)

    valor = ctk.CTkEntry(
        frame_nova_taxa,
        placeholder_text="Valor"
    )
    valor.pack(side="left", padx=5, pady=5)

    def atualizar_taxas():

        for widget in lista_taxas.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, distancia_km, valor
            FROM taxas_distancia
            ORDER BY distancia_km
        """)

        taxas = cursor.fetchall()

        conn.close()

        if not taxas:

            ctk.CTkLabel(
                lista_taxas,
                text="Nenhuma taxa cadastrada."
            ).pack(pady=10)

            return

        for taxa in taxas:

            linha = ctk.CTkFrame(lista_taxas)
            linha.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(
                linha,
                text=f"Até {taxa[1]} KM → R$ {taxa[2]:.2f}"
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                linha,
                text="Excluir",
                width=80,
                fg_color="#8B0000",
                hover_color="#A00000",
                command=lambda id_taxa=taxa[0]: excluir_taxa(id_taxa)
            ).pack(side="right", padx=5)

    def adicionar_taxa():

        try:

            km = float(
                distancia.get().replace(",", ".")
            )

            preco = float(
                valor.get().replace(",", ".")
            )

        except:

            mensagem.configure(
                text="Valores inválidos."
            )

            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO taxas_distancia
            (distancia_km, valor)
            VALUES (?, ?)
        """, (km, preco))

        conn.commit()
        conn.close()

        distancia.delete(0, "end")
        valor.delete(0, "end")

        atualizar_taxas()

        mensagem.configure(
            text="Taxa adicionada."
        )

    def excluir_taxa(id_taxa):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM taxas_distancia
            WHERE id = ?
        """, (id_taxa,))

        conn.commit()
        conn.close()

        atualizar_taxas()

        mensagem.configure(
            text="Taxa removida."
        )

    ctk.CTkButton(
        frame_nova_taxa,
        text="Adicionar Taxa",
        command=adicionar_taxa
    ).pack(side="left", padx=5)

    # =========================
    # ABA APARÊNCIA
    # =========================
    ctk.CTkLabel(
        aba_aparencia,
        text="Aparência do Sistema",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    modo_var = ctk.StringVar(
        value=tema_atual.get("appearance", "dark")
    )

    ctk.CTkLabel(
        aba_aparencia,
        text="Modo"
    ).pack(pady=5)

    ctk.CTkOptionMenu(
        aba_aparencia,
        values=["dark", "light"],
        variable=modo_var
    ).pack(pady=10)

    ctk.CTkLabel(
        aba_aparencia,
        text="Cor principal"
    ).pack(pady=5)

    cores_tema = {
        "Azul": "#2563EB",
        "Verde": "#16A34A",
        "Roxo": "#7C3AED",
        "Vermelho": "#DC2626",
        "Laranja": "#EA580C",
        "Ciano": "#0891B2"
    }

    nome_cor_padrao = "Azul"

    for nome, codigo in cores_tema.items():

        if codigo == tema_atual.get("primary"):
            nome_cor_padrao = nome
            break

    nome_cor_var = ctk.StringVar(
        value=nome_cor_padrao
    )

    menu_cores = ctk.CTkOptionMenu(
        aba_aparencia,
        values=list(cores_tema.keys()),
        variable=nome_cor_var
    )

    menu_cores.pack(pady=10)

    ctk.CTkLabel(
        aba_aparencia,
        text="Escolha a cor do sistema"
    ).pack(pady=5)

    def salvar_aparencia():

        cor_escolhida = cores_tema[
            nome_cor_var.get()
        ]

        salvar_tema({
            "appearance": modo_var.get(),
            "primary": cor_escolhida
        })

        mensagem.configure(
            text="Aparência salva com sucesso. Reinicie o sistema."
        )

    ctk.CTkButton(
        aba_aparencia,
        text="Salvar Aparência",
        command=salvar_aparencia
    ).pack(pady=20)

    carregar_configuracoes_loja()
    atualizar_taxas()