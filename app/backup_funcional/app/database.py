import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "crm.db"


def conectar():
    DATA_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # =========================
    # CLIENTES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        endereco TEXT,
        bairro TEXT,
        observacoes TEXT,
        lista_negra INTEGER DEFAULT 0
    )
    """)

    # =========================
    # PRODUTOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT,
        tamanho TEXT,
        preco REAL NOT NULL,
        disponivel INTEGER DEFAULT 1
    )
    """)

    # =========================
    # INGREDIENTES DOS PRODUTOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes_produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        ingrediente TEXT NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    # =========================
    # ADICIONAIS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adicionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)

    # =========================
    # CONFIGURAÇÕES DA LOJA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes_loja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_loja TEXT,
        endereco_loja TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # =========================
    # TAXAS POR DISTÂNCIA
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taxas_distancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        distancia_km REAL NOT NULL,
        valor REAL NOT NULL
    )
    """)

    # =========================
    # TAXAS ANTIGAS POR BAIRRO
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taxas_entrega (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bairro TEXT NOT NULL UNIQUE,
        valor REAL NOT NULL
    )
    """)

    # =========================
    # PEDIDOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        taxa_entrega REAL NOT NULL,
        total REAL NOT NULL,
        status TEXT NOT NULL,
        data_hora TEXT NOT NULL,
        observacao TEXT,
        forma_pagamento TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    """)

    # =========================
    # ITENS DO PEDIDO
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    # =========================
    # ADICIONAIS DOS ITENS/PEDIDOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_adicionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        adicional_id INTEGER,
        nome_adicional TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY (adicional_id) REFERENCES adicionais(id)
    )
    """)

    # =========================
    # MIGRAÇÕES
    # =========================
    try:
        cursor.execute("""
            ALTER TABLE clientes
            ADD COLUMN lista_negra INTEGER DEFAULT 0
        """)
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("""
            ALTER TABLE pedidos
            ADD COLUMN observacao TEXT
        """)
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("""
            ALTER TABLE pedidos
            ADD COLUMN forma_pagamento TEXT
        """)
    except sqlite3.OperationalError:
        pass

    # =========================
    # TAXAS PADRÃO POR DISTÂNCIA
    # =========================
    taxas_distancia = [
        (2, 5.00),
        (4, 8.00),
        (6, 12.00)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO taxas_distancia
        (distancia_km, valor)
        VALUES (?, ?)
    """, taxas_distancia)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco atualizado com forma de pagamento!")