
# CRM Atendimento

<p align="center">
  <img src="screenshots/logo.png" width="500">
</p>

# PedidoFlow

Sistema desktop de gestão para delivery com autenticação segura, dashboard financeiro, pedidos, usuários e backup local.
Sistema desktop para gerenciamento de atendimento e pedidos.

---

# Funcionalidades

- Cadastro de clientes
- Cadastro de produtos
- Cadastro de adicionais
- Pedidos completos
- Pizza meio a meio
- Controle de ingredientes
- Taxa de entrega automática
- Dashboard
- Fechamento financeiro
- Histórico de pedidos
- Envio para WhatsApp
- Geração de TXT
- Cupom formatado para impressão térmica

---

# Tecnologias

- Python
- CustomTkinter
- SQLite
- PyInstaller

---

# Estrutura

```text
CRM Atendimento/
│
├── app/
├── backup_funcional/
├── requirements.txt
└── README.md
```

---

# Executar em Python

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
python gui.py
```

---

# Gerar executável

Dentro da pasta `app`:

```bash
python -m PyInstaller --onefile --windowed --name "CRM Atendimento" gui.py
```

Executável gerado em:

```text
dist/
```

---

# Estrutura automática criada

O sistema cria automaticamente:

```text
data/
pedidos_txt/
cupons_formatados/
backups/
config/
```

---

# Banco de dados

Banco local SQLite:

```text
data/crm.db
```

---

# Impressão térmica

O sistema gera cupons formatados automaticamente em:

```text
cupons_formatados/
```

Preparado para futura integração com impressoras térmicas.

---

# Backup recomendado

Recomendado realizar backup periódico das pastas:

```text
data/
pedidos_txt/
cupons_formatados/
```

---

# Observações

Sistema desenvolvido para funcionamento local/offline.

Preparado para:
- expansão futura
- melhorias visuais
- impressão real
- deploy portátil
- possível migração web futuramente

# 📸 Screenshots

## Login

![Login](screenshots/login.png)

---

## Dashboard

![Dashboard](screenshots/dashboard.png)

---

## Pedidos

![Pedidos](screenshots/pedidos.png)

---

## Usuários

![Usuarios](screenshots/usuarios.png)

---

## Configurações

![Configuracoes](screenshots/configuracoes.png)