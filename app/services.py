import bcrypt
from database import conectar
from datetime import datetime
from paths import PEDIDOS_DIR
from localizacao import calcular_entrega_por_endereco


# =========================
# SENHAS
# =========================
def gerar_hash_senha(senha):
    senha_bytes = senha.encode("utf-8")
    hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_senha.decode("utf-8")


def verificar_senha(senha_digitada, hash_salvo):
    return bcrypt.checkpw(
        senha_digitada.encode("utf-8"),
        hash_salvo.encode("utf-8")
    )


# =========================
# CLIENTES
# =========================
def adicionar_cliente(nome, telefone, endereco, bairro, observacoes, lista_negra=0):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (nome, telefone, endereco, bairro, observacoes, lista_negra)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, telefone, endereco, bairro, observacoes, lista_negra))

    conn.commit()
    conn.close()


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")

    dados = cursor.fetchall()

    conn.close()
    return dados


def buscar_cliente_por_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    cliente = cursor.fetchone()

    conn.close()
    return cliente


def editar_cliente(cliente_id, nome, telefone, endereco, bairro, observacoes, lista_negra):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nome = ?, telefone = ?, endereco = ?, bairro = ?, observacoes = ?, lista_negra = ?
        WHERE id = ?
    """, (nome, telefone, endereco, bairro, observacoes, lista_negra, cliente_id))

    conn.commit()
    conn.close()


def marcar_cliente_lista_negra(cliente_id, lista_negra=1):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET lista_negra = ?
        WHERE id = ?
    """, (lista_negra, cliente_id))

    conn.commit()
    conn.close()


# =========================
# PRODUTOS
# =========================
def adicionar_produto(nome, categoria, tamanho, preco, ingredientes="", disponivel=1):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produtos (nome, categoria, tamanho, preco, disponivel)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, categoria, tamanho, preco, disponivel))

    produto_id = cursor.lastrowid

    ingredientes_lista = [
        i.strip()
        for i in ingredientes.split(",")
        if i.strip()
    ]

    for ingrediente in ingredientes_lista:
        cursor.execute("""
            INSERT INTO ingredientes_produto (produto_id, ingrediente)
            VALUES (?, ?)
        """, (produto_id, ingrediente))

    conn.commit()
    conn.close()


def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM produtos
        WHERE disponivel = 1
    """)

    dados = cursor.fetchall()

    conn.close()
    return dados


def buscar_produto_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM produtos
        WHERE id = ?
    """, (produto_id,))

    produto = cursor.fetchone()

    conn.close()
    return produto


def listar_ingredientes_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ingrediente
        FROM ingredientes_produto
        WHERE produto_id = ?
    """, (produto_id,))

    dados = cursor.fetchall()

    conn.close()

    return [d[0] for d in dados]


def editar_produto(produto_id, nome, categoria, tamanho, preco, ingredientes=""):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE produtos
        SET nome = ?, categoria = ?, tamanho = ?, preco = ?
        WHERE id = ?
    """, (nome, categoria, tamanho, preco, produto_id))

    cursor.execute("""
        DELETE FROM ingredientes_produto
        WHERE produto_id = ?
    """, (produto_id,))

    ingredientes_lista = [
        i.strip()
        for i in ingredientes.split(",")
        if i.strip()
    ]

    for ingrediente in ingredientes_lista:
        cursor.execute("""
            INSERT INTO ingredientes_produto (produto_id, ingrediente)
            VALUES (?, ?)
        """, (produto_id, ingrediente))

    conn.commit()
    conn.close()


def inativar_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE produtos
        SET disponivel = 0
        WHERE id = ?
    """, (produto_id,))

    conn.commit()
    conn.close()


# =========================
# ADICIONAIS
# =========================
def adicionar_adicional(nome, valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO adicionais (nome, valor, ativo)
        VALUES (?, ?, 1)
    """, (nome, valor))

    conn.commit()
    conn.close()


def listar_adicionais():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, valor
        FROM adicionais
        WHERE ativo = 1
        ORDER BY nome
    """)

    dados = cursor.fetchall()

    conn.close()
    return dados


def editar_adicional(adicional_id, nome, valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE adicionais
        SET nome = ?, valor = ?
        WHERE id = ?
    """, (nome, valor, adicional_id))

    conn.commit()
    conn.close()


def inativar_adicional(adicional_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE adicionais
        SET ativo = 0
        WHERE id = ?
    """, (adicional_id,))

    conn.commit()
    conn.close()


# =========================
# ENTREGA
# =========================
def calcular_taxa_cliente(cliente_id):
    cliente = buscar_cliente_por_id(cliente_id)

    if not cliente:
        return None, None, "Cliente não encontrado."

    endereco = cliente[3]

    if not endereco:
        return None, None, "Cliente sem endereço cadastrado."

    distancia, taxa, mensagem = calcular_entrega_por_endereco(endereco)

    return distancia, taxa, mensagem


# =========================
# PEDIDOS
# =========================
def calcular_subtotal_itens(itens):
    subtotal = 0

    for item in itens:
        adicionais = item.get("adicionais", [])
        total_adicionais = sum(a["valor"] for a in adicionais)

        if item.get("tipo") == "meio_a_meio":
            produto_1 = buscar_produto_por_id(item["produto_id"])
            produto_2 = buscar_produto_por_id(item["produto_id_2"])

            if not produto_1 or not produto_2:
                continue

            preco = max(produto_1[4], produto_2[4])
            subtotal += (preco + total_adicionais) * item["quantidade"]

        else:
            produto = buscar_produto_por_id(item["produto_id"])

            if not produto:
                continue

            subtotal += (produto[4] + total_adicionais) * item["quantidade"]

    return subtotal


def criar_pedido(cliente_id, itens, observacao="", forma_pagamento="Não informado"):
    cliente = buscar_cliente_por_id(cliente_id)

    if not cliente:
        return None, "Cliente não encontrado."

    subtotal = calcular_subtotal_itens(itens)

    distancia, taxa, msg_taxa = calcular_taxa_cliente(cliente_id)

    if taxa is None:
        taxa = 0

    total = subtotal + taxa

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pedidos
        (cliente_id, subtotal, taxa_entrega, total, status, data_hora, observacao, forma_pagamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cliente_id,
        subtotal,
        taxa,
        total,
        "Aberto",
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        observacao,
        forma_pagamento
    ))

    pedido_id = cursor.lastrowid

    for item in itens:
        adicionais = item.get("adicionais", [])

        if item.get("tipo") == "meio_a_meio":
            produto_1 = buscar_produto_por_id(item["produto_id"])
            produto_2 = buscar_produto_por_id(item["produto_id_2"])

            if not produto_1 or not produto_2:
                continue

            preco_unitario = max(produto_1[4], produto_2[4])

            cursor.execute("""
                INSERT INTO itens_pedido
                (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            """, (
                pedido_id,
                item["produto_id"],
                item["quantidade"],
                preco_unitario
            ))

            cursor.execute("""
                INSERT INTO itens_pedido
                (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            """, (
                pedido_id,
                item["produto_id_2"],
                item["quantidade"],
                0
            ))

        else:
            produto = buscar_produto_por_id(item["produto_id"])

            if not produto:
                continue

            cursor.execute("""
                INSERT INTO itens_pedido
                (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            """, (
                pedido_id,
                item["produto_id"],
                item["quantidade"],
                produto[4]
            ))

        for adicional in adicionais:
            cursor.execute("""
                INSERT INTO item_adicionais
                (pedido_id, adicional_id, nome_adicional, valor)
                VALUES (?, ?, ?, ?)
            """, (
                pedido_id,
                adicional.get("id"),
                adicional.get("nome"),
                adicional.get("valor")
            ))

    conn.commit()
    conn.close()

    return pedido_id, "Pedido criado com sucesso."


def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pedidos.id,
            clientes.nome,
            pedidos.total,
            pedidos.status,
            pedidos.data_hora,
            pedidos.observacao,
            pedidos.forma_pagamento
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        ORDER BY pedidos.id DESC
    """)

    dados = cursor.fetchall()

    conn.close()
    return dados


# =========================
# TEXTO PEDIDO
# =========================
def gerar_texto_pedido(pedido_id, cliente_id, itens, observacao="", forma_pagamento="Não informado"):
    cliente = buscar_cliente_por_id(cliente_id)

    linhas = []

    linhas.append(f"====== PEDIDO #{pedido_id} ======")
    linhas.append(f"Cliente: {cliente[1]}")
    linhas.append(f"Telefone: {cliente[2]}")
    linhas.append(f"Endereço: {cliente[3]}")
    linhas.append(f"Bairro: {cliente[4]}")
    linhas.append(f"Pagamento: {forma_pagamento}")

    if len(cliente) > 6 and cliente[6] == 1:
        linhas.append("ATENÇÃO: CLIENTE NA LISTA NEGRA")

    linhas.append("")

    subtotal = 0

    for item in itens:
        adicionais = item.get("adicionais", [])
        total_adicionais = sum(a["valor"] for a in adicionais)

        if item.get("tipo") == "meio_a_meio":
            produto_1 = buscar_produto_por_id(item["produto_id"])
            produto_2 = buscar_produto_por_id(item["produto_id_2"])

            if not produto_1 or not produto_2:
                continue

            preco = max(produto_1[4], produto_2[4])
            total_item = (preco + total_adicionais) * item["quantidade"]
            subtotal += total_item

            linhas.append(f"Pizza Meio a Meio x{item['quantidade']} = R$ {total_item:.2f}")
            linhas.append(f"1/2 {produto_1[1]}")
            linhas.append(f"1/2 {produto_2[1]}")

        else:
            produto = buscar_produto_por_id(item["produto_id"])

            if not produto:
                continue

            total_item = (produto[4] + total_adicionais) * item["quantidade"]
            subtotal += total_item

            linhas.append(f"{produto[1]} x{item['quantidade']} = R$ {total_item:.2f}")

        removidos = item.get("sem_ingredientes", [])

        if removidos:
            linhas.append(f"Sem: {', '.join(removidos)}")

        if adicionais:
            for adicional in adicionais:
                linhas.append(f"+ {adicional['nome']} R$ {adicional['valor']:.2f}")

        linhas.append("")

    if observacao.strip():
        linhas.append(f"Obs: {observacao}")
        linhas.append("")

    distancia, taxa, mensagem = calcular_taxa_cliente(cliente_id)

    if taxa is None:
        taxa = 0

    total = subtotal + taxa

    linhas.append("---------------------")
    linhas.append(f"Subtotal: R$ {subtotal:.2f}")

    if distancia is not None:
        linhas.append(f"Distância: {distancia:.2f} km")

    linhas.append(f"Entrega: R$ {taxa:.2f}")
    linhas.append(f"TOTAL: R$ {total:.2f}")
    linhas.append("=====================")

    return "\n".join(linhas)


# =========================
# TXT / HISTÓRICO
# =========================
def salvar_pedido_txt(texto, pedido_id):
    caminho = PEDIDOS_DIR / f"pedido_{pedido_id}.txt"

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)

    return caminho


def ler_txt_pedido(pedido_id):
    caminho = PEDIDOS_DIR / f"pedido_{pedido_id}.txt"

    if not caminho.exists():
        return "TXT do pedido não encontrado."

    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


# =========================
# FECHAMENTO
# =========================
def fechamento_do_dia():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total)
        FROM pedidos
        WHERE status != 'Cancelado'
    """)
    total_vendido = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
    """)
    total_pedidos = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(taxa_entrega)
        FROM pedidos
    """)
    total_entrega = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status = 'Cancelado'
    """)
    cancelados = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT produtos.nome, SUM(itens_pedido.quantidade) as total
        FROM itens_pedido
        JOIN produtos ON itens_pedido.produto_id = produtos.id
        GROUP BY produtos.nome
        ORDER BY total DESC
        LIMIT 1
    """)
    mais_vendido = cursor.fetchone()

    cursor.execute("""
        SELECT forma_pagamento, SUM(total)
        FROM pedidos
        WHERE status != 'Cancelado'
        GROUP BY forma_pagamento
    """)
    por_pagamento = cursor.fetchall()

    conn.close()

    return {
        "total_vendido": total_vendido,
        "total_pedidos": total_pedidos,
        "total_entrega": total_entrega,
        "cancelados": cancelados,
        "mais_vendido": mais_vendido[0] if mais_vendido else "Nenhum",
        "por_pagamento": por_pagamento
    }


# =========================
# DASHBOARD
# =========================
def dados_dashboard():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total)
        FROM pedidos
        WHERE status != 'Cancelado'
    """)
    total_vendido = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
    """)
    quantidade_pedidos = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(taxa_entrega)
        FROM pedidos
    """)
    total_entregas = cursor.fetchone()[0] or 0

    ticket_medio = 0

    if quantidade_pedidos > 0:
        ticket_medio = total_vendido / quantidade_pedidos

    cursor.execute("""
        SELECT produtos.nome, SUM(itens_pedido.quantidade) as total
        FROM itens_pedido
        JOIN produtos ON itens_pedido.produto_id = produtos.id
        GROUP BY produtos.nome
        ORDER BY total DESC
        LIMIT 1
    """)
    mais_vendido = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM clientes
    """)
    total_clientes = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM produtos
        WHERE disponivel = 1
    """)
    total_produtos = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT forma_pagamento, SUM(total)
        FROM pedidos
        WHERE status != 'Cancelado'
        GROUP BY forma_pagamento
    """)
    por_pagamento = cursor.fetchall()

    cursor.execute("""
        SELECT
            pedidos.id,
            clientes.nome,
            pedidos.total,
            pedidos.forma_pagamento
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        ORDER BY pedidos.id DESC
        LIMIT 5
    """)
    ultimos_pedidos = cursor.fetchall()

    cursor.execute("""
        SELECT
            produtos.nome,
            SUM(itens_pedido.quantidade) as total
        FROM itens_pedido
        JOIN produtos ON itens_pedido.produto_id = produtos.id
        GROUP BY produtos.nome
        ORDER BY total DESC
        LIMIT 5
    """)
    ranking_produtos = cursor.fetchall()

    conn.close()

    return {
        "total_vendido": total_vendido,
        "quantidade_pedidos": quantidade_pedidos,
        "ticket_medio": ticket_medio,
        "total_entregas": total_entregas,
        "mais_vendido": mais_vendido[0] if mais_vendido else "Nenhum",
        "total_clientes": total_clientes,
        "total_produtos": total_produtos,
        "por_pagamento": por_pagamento,
        "ultimos_pedidos": ultimos_pedidos,
        "ranking_produtos": ranking_produtos
    }


# =========================
# LOGIN / USUÁRIOS
# =========================
def validar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, usuario, senha, tipo
        FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    usuario_banco = cursor.fetchone()

    conn.close()

    if not usuario_banco:
        return None

    senha_hash = usuario_banco[2]

    try:
        senha_ok = verificar_senha(senha, senha_hash)
    except Exception:
        return None

    if not senha_ok:
        return None

    return (
        usuario_banco[0],
        usuario_banco[1],
        usuario_banco[3]
    )


def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, usuario, tipo
        FROM usuarios
        ORDER BY usuario
    """)

    dados = cursor.fetchall()

    conn.close()
    return dados


def criar_usuario(usuario, senha, tipo="Atendente"):
    conn = conectar()
    cursor = conn.cursor()

    try:
        senha_hash = gerar_hash_senha(senha)

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, senha, tipo)
            VALUES (?, ?, ?)
        """, (usuario, senha_hash, tipo))

        conn.commit()

        return True, "Usuário criado com sucesso."

    except Exception as erro:
        return False, str(erro)

    finally:
        conn.close()


def excluir_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (usuario_id,))

    conn.commit()
    conn.close()