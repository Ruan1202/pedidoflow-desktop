import shutil
from datetime import datetime
from paths import DATA_DIR, BACKUP_DIR


def gerar_backup_banco():
    banco_origem = DATA_DIR / "crm.db"

    if not banco_origem.exists():
        return False, "Banco de dados não encontrado."

    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_backup = f"backup_crm_{data_hora}.db"
    caminho_backup = BACKUP_DIR / nome_backup

    try:
        shutil.copy2(banco_origem, caminho_backup)
        return True, f"Backup criado com sucesso:\n{caminho_backup}"

    except Exception as erro:
        return False, f"Erro ao criar backup:\n{erro}"


def restaurar_backup_banco(caminho_backup):
    banco_destino = DATA_DIR / "crm.db"

    if not caminho_backup:
        return False, "Nenhum arquivo selecionado."

    try:
        caminho_backup = str(caminho_backup)

        if not caminho_backup.endswith(".db"):
            return False, "Selecione um arquivo .db válido."

        if banco_destino.exists():
            data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_antes_restaurar = BACKUP_DIR / f"backup_antes_restaurar_{data_hora}.db"
            shutil.copy2(banco_destino, backup_antes_restaurar)

        shutil.copy2(caminho_backup, banco_destino)

        return True, "Backup restaurado com sucesso.\nFeche e abra o sistema novamente."

    except Exception as erro:
        return False, f"Erro ao restaurar backup:\n{erro}"