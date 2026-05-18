from services import (
    listar_clientes,
    listar_produtos,
    listar_adicionais,
    criar_pedido,
    gerar_texto_pedido,
    salvar_pedido_txt,
    listar_ingredientes_produto,
    calcular_taxa_cliente
)

import customtkinter as ctk
import webbrowser
import urllib.parse
from helpers.impressao import simular_impressao

def tela_pedidos(area_conteudo):

    for widget in area_conteudo.winfo_children():
        widget.destroy()

    itens = []
    checkboxes_ingredientes = []
    checkboxes_adicionais = []

    ultimo_pedido = {
        "texto": "",
        "telefone": ""
    }

    ctk.CTkLabel(
        area_conteudo,
        text="Pedidos",
        font=("Arial", 26, "bold")
    ).pack(pady=10)

    frame_principal = ctk.CTkFrame(area_conteudo)
    frame_principal.pack(fill="both", expand=True, padx=15, pady=10)

    frame_esquerda = ctk.CTkScrollableFrame(frame_principal, width=360)
    frame_esquerda.pack(side="left", fill="y", padx=10, pady=10)

    frame_direita = ctk.CTkFrame(frame_principal)
    frame_direita.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    clientes = listar_clientes()
    produtos = listar_produtos()
    adicionais = listar_adicionais()

    lista_clientes = [f"{c[0]} - {c[1]}" for c in clientes]
    lista_produtos = [f"{p[0]} - {p[1]}" for p in produtos]
    formas_pagamento = ["PIX", "Dinheiro", "Débito", "Crédito"]

    cliente_var = ctk.StringVar()
    produto_var = ctk.StringVar()
    produto_2_var = ctk.StringVar()
    pagamento_var = ctk.StringVar(value="PIX")
    meio_a_meio_var = ctk.IntVar(value=0)

    if lista_clientes:
        cliente_var.set(lista_clientes[0])

    if lista_produtos:
        produto_var.set(lista_produtos[0])
        produto_2_var.set(lista_produtos[0])

    # =========================
    # CLIENTE
    # =========================
    frame_cliente = ctk.CTkFrame(frame_esquerda)
    frame_cliente.pack(fill="x", pady=5)

    ctk.CTkLabel(
        frame_cliente,
        text="Cliente",
        font=("Arial", 18, "bold")
    ).pack(pady=5)

    ctk.CTkOptionMenu(
        frame_cliente,
        values=lista_clientes if lista_clientes else ["Nenhum cliente"],
        variable=cliente_var
    ).pack(padx=10, pady=10)

    # =========================
    # ENTREGA
    # =========================
    frame_entrega = ctk.CTkFrame(frame_esquerda)
    frame_entrega.pack(fill="x", pady=5)

    ctk.CTkLabel(
        frame_entrega,
        text="Entrega",
        font=("Arial", 18, "bold")
    ).pack(pady=5)

    info_entrega = ctk.CTkTextbox(frame_entrega, width=320, height=80)
    info_entrega.pack(padx=10, pady=10)

    # =========================
    # PAGAMENTO
    # =========================
    frame_pagamento = ctk.CTkFrame(frame_esquerda)
    frame_pagamento.pack(fill="x", pady=5)

    ctk.CTkLabel(
        frame_pagamento,
        text="Pagamento",
        font=("Arial", 18, "bold")
    ).pack(pady=5)

    ctk.CTkOptionMenu(
        frame_pagamento,
        values=formas_pagamento,
        variable=pagamento_var,
        command=lambda _: atualizar_visualizacao()
    ).pack(padx=10, pady=10)

    # =========================
    # PRODUTO
    # =========================
    frame_produto = ctk.CTkFrame(frame_esquerda)
    frame_produto.pack(fill="x", pady=5)

    ctk.CTkLabel(
        frame_produto,
        text="Produto",
        font=("Arial", 18, "bold")
    ).pack(pady=5)

    ctk.CTkOptionMenu(
        frame_produto,
        values=lista_produtos if lista_produtos else ["Nenhum produto"],
        variable=produto_var
    ).pack(padx=10, pady=8)

    check_meio = ctk.CTkCheckBox(
        frame_produto,
        text="Meio a meio",
        variable=meio_a_meio_var,
        command=lambda: alternar_meio_a_meio()
    )
    check_meio.pack(padx=10, pady=5)

    label_produto_2 = ctk.CTkLabel(frame_produto, text="Segundo sabor")

    menu_produto_2 = ctk.CTkOptionMenu(
        frame_produto,
        values=lista_produtos if lista_produtos else ["Nenhum produto"],
        variable=produto_2_var
    )

    quantidade = ctk.CTkEntry(frame_produto, placeholder_text="Quantidade")
    quantidade.pack(fill="x", padx=10, pady=5)

    observacao = ctk.CTkEntry(frame_produto, placeholder_text="Observação geral")
    observacao.pack(fill="x", padx=10, pady=5)

    # =========================
    # INGREDIENTES
    # =========================
    frame_checklist = ctk.CTkFrame(frame_esquerda)
    frame_checklist.pack(fill="x", pady=5)

    ctk.CTkLabel(
        frame_checklist,
        text="Ingredientes",
        font=("Arial", 18, "bold")
    ).pack(pady=5)

    frame_checks = ctk.CTkScrollableFrame(frame_checklist, width=320, height=130)
    frame_checks.pack(fill="both", expand=True, padx=10, pady=10)

    # =========================
    # ADICIONAIS
    # =========================
    frame_adicionais = ctk.CTkFrame(frame_esquerda)
    frame_adicionais.pack(fill="x", pady=5)

    ctk.CTkLabel(
        frame_adicionais,
        text="Adicionais",
        font=("Arial", 18, "bold")
    ).pack(pady=5)

    frame_checks_adicionais = ctk.CTkScrollableFrame(
        frame_adicionais,
        width=320,
        height=160
    )
    frame_checks_adicionais.pack(fill="both", expand=True, padx=10, pady=10)

    # =========================
    # RESUMO
    # =========================
    ctk.CTkLabel(
        frame_direita,
        text="Resumo do Pedido",
        font=("Arial", 22, "bold")
    ).pack(pady=10)

    visualizacao = ctk.CTkTextbox(frame_direita)
    visualizacao.pack(fill="both", expand=True, padx=10, pady=10)

    mensagem = ctk.CTkLabel(frame_direita, text="")
    mensagem.pack(pady=5)

    # =========================
    # FUNÇÕES
    # =========================
    def buscar_produto_lista(produto_id):
        return next((p for p in produtos if p[0] == produto_id), None)

    def obter_id(valor):
        return int(valor.split(" - ")[0])

    def atualizar_entrega():
        info_entrega.delete("1.0", "end")

        try:
            cliente_id = obter_id(cliente_var.get())
        except:
            info_entrega.insert("1.0", "Cliente inválido.")
            return

        distancia, taxa, msg = calcular_taxa_cliente(cliente_id)

        if taxa is None:
            info_entrega.insert("1.0", msg)
            return

        info_entrega.insert(
            "1.0",
            f"Distância: {distancia:.2f} km\nTaxa: R$ {taxa:.2f}"
        )

        atualizar_visualizacao()

    def alternar_meio_a_meio():
        if meio_a_meio_var.get() == 1:
            label_produto_2.pack(pady=2)
            menu_produto_2.pack(padx=10, pady=8)
        else:
            label_produto_2.pack_forget()
            menu_produto_2.pack_forget()

        atualizar_visualizacao()

    def carregar_ingredientes(*args):
        for widget in frame_checks.winfo_children():
            widget.destroy()

        checkboxes_ingredientes.clear()

        try:
            produto_id = obter_id(produto_var.get())
        except:
            return

        ingredientes = listar_ingredientes_produto(produto_id)

        if not ingredientes:
            ctk.CTkLabel(
                frame_checks,
                text="Sem ingredientes."
            ).pack(anchor="w", padx=10, pady=5)
            return

        for ingrediente in ingredientes:
            var = ctk.IntVar(value=1)

            ctk.CTkCheckBox(
                frame_checks,
                text=ingrediente,
                variable=var
            ).pack(anchor="w", padx=10, pady=3)

            checkboxes_ingredientes.append({
                "nome": ingrediente,
                "var": var
            })

    def carregar_adicionais():
        for widget in frame_checks_adicionais.winfo_children():
            widget.destroy()

        checkboxes_adicionais.clear()

        if not adicionais:
            ctk.CTkLabel(
                frame_checks_adicionais,
                text="Nenhum adicional cadastrado."
            ).pack(anchor="w", padx=10, pady=5)
            return

        for adicional in adicionais:
            adicional_id = adicional[0]
            nome = adicional[1]
            valor = adicional[2]

            var = ctk.IntVar(value=0)

            ctk.CTkCheckBox(
                frame_checks_adicionais,
                text=f"{nome} - R$ {valor:.2f}",
                variable=var,
                command=atualizar_visualizacao
            ).pack(anchor="w", padx=10, pady=3)

            checkboxes_adicionais.append({
                "id": adicional_id,
                "nome": nome,
                "valor": valor,
                "var": var
            })

    def obter_removidos():
        return [
            item["nome"]
            for item in checkboxes_ingredientes
            if item["var"].get() == 0
        ]

    def obter_adicionais_selecionados():
        return [
            {
                "id": item["id"],
                "nome": item["nome"],
                "valor": item["valor"]
            }
            for item in checkboxes_adicionais
            if item["var"].get() == 1
        ]

    def resetar_checklist():
        for item in checkboxes_ingredientes:
            item["var"].set(1)

    def resetar_adicionais():
        for item in checkboxes_adicionais:
            item["var"].set(0)

    def calcular_preco_item(item):
        valor_adicionais = sum(a["valor"] for a in item.get("adicionais", []))

        if item.get("tipo") == "meio_a_meio":
            produto_1 = buscar_produto_lista(item["produto_id"])
            produto_2 = buscar_produto_lista(item["produto_id_2"])

            if not produto_1 or not produto_2:
                return 0

            return (max(produto_1[4], produto_2[4]) + valor_adicionais) * item["quantidade"]

        produto = buscar_produto_lista(item["produto_id"])

        if not produto:
            return 0

        return (produto[4] + valor_adicionais) * item["quantidade"]

    def calcular_totais():
        subtotal = sum(calcular_preco_item(item) for item in itens)

        taxa = 0

        try:
            cliente_id = obter_id(cliente_var.get())
            _, taxa_calc, _ = calcular_taxa_cliente(cliente_id)

            if taxa_calc:
                taxa = taxa_calc
        except:
            pass

        return subtotal, taxa, subtotal + taxa

    def atualizar_visualizacao():
        visualizacao.delete("1.0", "end")

        linhas = []

        linhas.append(f"Pagamento: {pagamento_var.get()}")
        linhas.append("")

        if not itens:
            linhas.append("Nenhum item no pedido.")
        else:
            for item in itens:
                if item.get("tipo") == "meio_a_meio":
                    produto_1 = buscar_produto_lista(item["produto_id"])
                    produto_2 = buscar_produto_lista(item["produto_id_2"])

                    if not produto_1 or not produto_2:
                        continue

                    valor_item = calcular_preco_item(item)

                    linhas.append(
                        f"Pizza Meio a Meio x{item['quantidade']} = R$ {valor_item:.2f}"
                    )
                    linhas.append(f"1/2 {produto_1[1]}")
                    linhas.append(f"1/2 {produto_2[1]}")

                else:
                    produto = buscar_produto_lista(item["produto_id"])

                    if not produto:
                        continue

                    valor_item = calcular_preco_item(item)
                    linhas.append(
                        f"{produto[1]} x{item['quantidade']} = R$ {valor_item:.2f}"
                    )

                removidos = item.get("sem_ingredientes", [])

                if removidos:
                    linhas.append(f"Sem: {', '.join(removidos)}")

                adicionais_item = item.get("adicionais", [])

                if adicionais_item:
                    for adicional in adicionais_item:
                        linhas.append(f"+ {adicional['nome']} R$ {adicional['valor']:.2f}")

                linhas.append("")

        if observacao.get().strip():
            linhas.append(f"Obs: {observacao.get()}")
            linhas.append("")

        subtotal, taxa, total = calcular_totais()

        linhas.append("---------------------")
        linhas.append(f"Subtotal: R$ {subtotal:.2f}")
        linhas.append(f"Entrega: R$ {taxa:.2f}")
        linhas.append(f"TOTAL: R$ {total:.2f}")

        visualizacao.insert("1.0", "\n".join(linhas))

    def adicionar_item():
        mensagem.configure(text="")

        try:
            produto_id = obter_id(produto_var.get())
            qtd = int(quantidade.get())
        except:
            mensagem.configure(text="Quantidade ou produto inválido.")
            return

        if qtd <= 0:
            mensagem.configure(text="Quantidade inválida.")
            return

        removidos = obter_removidos()
        adicionais_selecionados = obter_adicionais_selecionados()

        if meio_a_meio_var.get() == 1:
            try:
                produto_id_2 = obter_id(produto_2_var.get())
            except:
                mensagem.configure(text="Selecione o segundo sabor.")
                return

            if produto_id == produto_id_2:
                mensagem.configure(text="Escolha dois sabores diferentes para meio a meio.")
                return

            itens.append({
                "tipo": "meio_a_meio",
                "produto_id": produto_id,
                "produto_id_2": produto_id_2,
                "quantidade": qtd,
                "sem_ingredientes": removidos,
                "adicionais": adicionais_selecionados
            })

        else:
            itens.append({
                "tipo": "normal",
                "produto_id": produto_id,
                "quantidade": qtd,
                "sem_ingredientes": removidos,
                "adicionais": adicionais_selecionados
            })

        quantidade.delete(0, "end")
        resetar_checklist()
        resetar_adicionais()
        atualizar_visualizacao()

        mensagem.configure(text="Item adicionado.")

    def confirmar_pedido():
        mensagem.configure(text="")

        try:
            cliente_id = obter_id(cliente_var.get())
        except:
            mensagem.configure(text="Cliente inválido.")
            return

        if not itens:
            mensagem.configure(text="Adicione itens.")
            return

        forma_pagamento = pagamento_var.get()

        pedido_id, msg = criar_pedido(
            cliente_id,
            itens,
            observacao.get(),
            forma_pagamento
        )

        if not pedido_id:
            mensagem.configure(text=msg)
            return

        texto = gerar_texto_pedido(
            pedido_id,
            cliente_id,
            itens,
            observacao.get(),
            forma_pagamento
        )

        salvar_pedido_txt(texto, pedido_id)
        simular_impressao(texto, pedido_id)

        cliente = next((c for c in clientes if c[0] == cliente_id), None)

        ultimo_pedido["texto"] = texto
        ultimo_pedido["telefone"] = cliente[2] if cliente else ""

        visualizacao.delete("1.0", "end")
        visualizacao.insert("1.0", texto)

        mensagem.configure(text=f"Pedido #{pedido_id} confirmado!")

        itens.clear()
        quantidade.delete(0, "end")
        observacao.delete(0, "end")
        resetar_checklist()
        resetar_adicionais()

    def limpar_pedido():
        itens.clear()
        quantidade.delete(0, "end")
        observacao.delete(0, "end")
        resetar_checklist()
        resetar_adicionais()
        atualizar_visualizacao()
        mensagem.configure(text="")

    def enviar_whatsapp():
        texto = ultimo_pedido["texto"]
        telefone = ultimo_pedido["telefone"]

        if not texto:
            mensagem.configure(text="Nenhum pedido confirmado para enviar.")
            return

        if not telefone:
            mensagem.configure(text="Cliente sem telefone cadastrado.")
            return

        telefone = (
            telefone
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
            .replace("+", "")
        )

        if not telefone.startswith("55"):
            telefone = "55" + telefone

        mensagem_formatada = urllib.parse.quote(texto)
        url = f"https://wa.me/{telefone}?text={mensagem_formatada}"

        webbrowser.open(url)
        mensagem.configure(text="WhatsApp aberto com o resumo do pedido.")

    # =========================
    # EVENTOS
    # =========================
    produto_var.trace_add("write", carregar_ingredientes)
    cliente_var.trace_add("write", lambda *args: atualizar_entrega())
    observacao.bind("<KeyRelease>", lambda e: atualizar_visualizacao())

    # =========================
    # BOTÕES
    # =========================
    frame_botoes = ctk.CTkFrame(frame_direita)
    frame_botoes.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(
        frame_botoes,
        text="Adicionar Item",
        command=adicionar_item
    ).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(
        frame_botoes,
        text="Confirmar Pedido",
        command=confirmar_pedido
    ).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(
        frame_botoes,
        text="Enviar WhatsApp",
        command=enviar_whatsapp
    ).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(
        frame_botoes,
        text="Limpar Pedido",
        command=limpar_pedido
    ).pack(side="left", padx=5, pady=5)

    carregar_ingredientes()
    carregar_adicionais()
    atualizar_entrega()
    atualizar_visualizacao()