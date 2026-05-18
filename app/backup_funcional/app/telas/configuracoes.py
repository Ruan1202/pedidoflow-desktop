import customtkinter as ctk
from database import conectar


def tela_configuracoes(area_conteudo):

    for widget in area_conteudo.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        area_conteudo,
        text="Configurações da Loja",
        font=("Arial", 24, "bold")
    ).pack(pady=10)

    frame = ctk.CTkFrame(area_conteudo)
    frame.pack(fill="x", padx=20, pady=10)

    # =========================
    # CAMPOS LOJA
    # =========================
    nome_loja = ctk.CTkEntry(frame, placeholder_text="Nome da loja")
    nome_loja.pack(fill="x", padx=10, pady=5)

    endereco_loja = ctk.CTkEntry(frame, placeholder_text="Endereço da loja")
    endereco_loja.pack(fill="x", padx=10, pady=5)

    latitude = ctk.CTkEntry(frame, placeholder_text="Latitude")
    latitude.pack(fill="x", padx=10, pady=5)

    longitude = ctk.CTkEntry(frame, placeholder_text="Longitude")
    longitude.pack(fill="x", padx=10, pady=5)

    mensagem = ctk.CTkLabel(area_conteudo, text="")
    mensagem.pack(pady=5)

    # =========================
    # TAXAS
    # =========================
    frame_taxas = ctk.CTkFrame(area_conteudo)
    frame_taxas.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkLabel(
        frame_taxas,
        text="Taxas por Distância",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    lista_taxas = ctk.CTkScrollableFrame(frame_taxas)
    lista_taxas.pack(fill="both", expand=True, padx=10, pady=10)

    frame_nova_taxa = ctk.CTkFrame(frame_taxas)
    frame_nova_taxa.pack(fill="x", padx=10, pady=10)

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

    # =========================
    # FUNÇÕES
    # =========================
    def carregar_configuracoes():

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

    def salvar_configuracoes():

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
            text="Configurações salvas com sucesso!"
        )

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

            texto = (
                f"Até {taxa[1]} KM → "
                f"R$ {taxa[2]:.2f}"
            )

            ctk.CTkLabel(
                linha,
                text=texto
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
            km = float(distancia.get().replace(",", "."))
            preco = float(valor.get().replace(",", "."))

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
            text="Taxa adicionada!"
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

    # =========================
    # BOTÕES
    # =========================
    botoes = ctk.CTkFrame(frame)
    botoes.pack(pady=10)

    ctk.CTkButton(
        botoes,
        text="Salvar Configurações",
        command=salvar_configuracoes
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        frame_nova_taxa,
        text="Adicionar Taxa",
        command=adicionar_taxa
    ).pack(side="left", padx=5)

    carregar_configuracoes()
    atualizar_taxas()