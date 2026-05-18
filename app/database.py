import sqlite3
import bcrypt
from paths import DATA_DIR


DB_PATH = DATA_DIR / "crm.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def gerar_hash_senha(senha):
    senha_bytes = senha.encode("utf-8")
    hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_senha.decode("utf-8")


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes_produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        ingrediente TEXT NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adicionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes_loja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_loja TEXT,
        endereco_loja TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taxas_distancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        distancia_km REAL NOT NULL,
        valor REAL NOT NULL
    )
    """)

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

    cursor.execute("""
        SELECT senha
        FROM usuarios
        WHERE usuario = 'admin'
    """)

    admin = cursor.fetchone()

    if not admin:
        senha_hash = gerar_hash_senha("admin")

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, senha, tipo)
            VALUES (?, ?, ?)
        """, (
            "admin",
            senha_hash,
            "Administrador"
        ))
    else:
        senha_atual = admin[0]

        if senha_atual == "admin":
            senha_hash = gerar_hash_senha("admin")

            cursor.execute("""
                UPDATE usuarios
                SET senha = ?
                WHERE usuario = 'admin'
            """, (senha_hash,))

    taxas = [
        (2, 5.00),
        (4, 8.00),
        (6, 12.00)
    ]

    for taxa in taxas:
        cursor.execute("""
            SELECT *
            FROM taxas_distancia
            WHERE distancia_km = ?
        """, (taxa[0],))

        existe = cursor.fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO taxas_distancia
                (distancia_km, valor)
                VALUES (?, ?)
            """, taxa)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado/atualizado com senha criptografada!")