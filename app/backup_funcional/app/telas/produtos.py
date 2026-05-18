from services import (
    adicionar_produto,
    listar_produtos,
    editar_produto,
    inativar_produto,
    listar_ingredientes_produto
)
import customtkinter as ctk


def tela_produtos(area_conteudo):
    for widget in area_conteudo.winfo_children():
        widget.destroy()

    produto_selecionado = {"id": None}

    ctk.CTkLabel(area_conteudo, text="Produtos", font=("Arial", 24)).pack(pady=10)

    frame = ctk.CTkFrame(area_conteudo)
    frame.pack(pady=10)

    nome = ctk.CTkEntry(frame, placeholder_text="Nome")
    nome.pack(pady=5)

    categoria = ctk.CTkEntry(frame, placeholder_text="Categoria")
    categoria.pack(pady=5)

    tamanho = ctk.CTkEntry(frame, placeholder_text="Tamanho")
    tamanho.pack(pady=5)

    preco = ctk.CTkEntry(frame, placeholder_text="Preço")
    preco.pack(pady=5)

    ingredientes = ctk.CTkTextbox(frame, width=320, height=90)
    ingredientes.pack(pady=5)
    ingredientes.insert("1.0", "Ingredientes separados por vírgula")

    mensagem = ctk.CTkLabel(area_conteudo, text="")
    mensagem.pack(pady=5)

    lista = ctk.CTkScrollableFrame(area_conteudo)
    lista.pack(fill="both", expand=True, padx=20, pady=10)

    def limpar_campos():
        produto_selecionado["id"] = None

        nome.delete(0, "end")
        categoria.delete(0, "end")
        tamanho.delete(0, "end")
        preco.delete(0, "end")
        ingredientes.delete("1.0", "end")
        ingredientes.insert("1.0", "Ingredientes separados por vírgula")

    def selecionar_produto(produto):
        produto_selecionado["id"] = produto[0]

        nome.delete(0, "end")
        categoria.delete(0, "end")
        tamanho.delete(0, "end")
        preco.delete(0, "end")
        ingredientes.delete("1.0", "end")

        nome.insert(0, produto[1])
        categoria.insert(0, produto[2] or "")
        tamanho.insert(0, produto[3] or "")
        preco.insert(0, str(produto[4]).replace(".", ","))

        lista_ingredientes = listar_ingredientes_produto(produto[0])
        ingredientes.insert("1.0", ", ".join(lista_ingredientes))

        mensagem.configure(text=f"Produto #{produto[0]} selecionado para edição.")

    def atualizar():
        for w in lista.winfo_children():
            w.destroy()

        produtos = listar_produtos()

        if not produtos:
            ctk.CTkLabel(lista, text="Nenhum produto cadastrado.").pack(anchor="w", padx=10, pady=5)
            return

        for p in produtos:
            linha = ctk.CTkFrame(lista)
            linha.pack(fill="x", padx=5, pady=4)

            ing = listar_ingredientes_produto(p[0])
            ing_texto = ", ".join(ing) if ing else "Sem ingredientes"

            texto = (
                f"{p[0]} - {p[1]} | {p[2]} | {p[3]} | R$ {p[4]:.2f}\n"
                f"Ingredientes: {ing_texto}"
            )

            ctk.CTkLabel(linha, text=texto, justify="left").pack(side="left", padx=10)

            ctk.CTkButton(
                linha,
                text="Editar",
                width=80,
                command=lambda produto=p: selecionar_produto(produto)
            ).pack(side="right", padx=5)

            ctk.CTkButton(
                linha,
                text="Excluir",
                width=80,
                fg_color="#8B0000",
                hover_color="#A00000",
                command=lambda produto_id=p[0]: excluir_produto(produto_id)
            ).pack(side="right", padx=5)

    def salvar():
        mensagem.configure(text="")

        try:
            valor = float(preco.get().replace(",", "."))
        except:
            mensagem.configure(text="Preço inválido.")
            return

        if not nome.get().strip():
            mensagem.configure(text="Informe o nome do produto.")
            return

        texto_ingredientes = ingredientes.get("1.0", "end").strip()

        if texto_ingredientes == "Ingredientes separados por vírgula":
            texto_ingredientes = ""

        if produto_selecionado["id"]:
            editar_produto(
                produto_selecionado["id"],
                nome.get(),
                categoria.get(),
                tamanho.get(),
                valor,
                texto_ingredientes
            )
            mensagem.configure(text="Produto atualizado com sucesso.")
        else:
            adicionar_produto(
                nome.get(),
                categoria.get(),
                tamanho.get(),
                valor,
                texto_ingredientes
            )
            mensagem.configure(text="Produto cadastrado com sucesso.")

        limpar_campos()
        atualizar()

    def excluir_produto(produto_id):
        inativar_produto(produto_id)
        mensagem.configure(text=f"Produto #{produto_id} removido da lista.")
        limpar_campos()
        atualizar()

    botoes = ctk.CTkFrame(frame)
    botoes.pack(pady=10)

    ctk.CTkButton(botoes, text="Salvar", command=salvar).pack(side="left", padx=5)
    ctk.CTkButton(botoes, text="Limpar", command=limpar_campos).pack(side="left", padx=5)

    atualizar()