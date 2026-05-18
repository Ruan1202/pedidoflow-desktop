from pathlib import Path
import sys
import os


def obter_base_path():
    if getattr(sys, "frozen", False):
        return Path(os.getenv("LOCALAPPDATA")) / "PedidoFlow"

    return Path(__file__).resolve().parent


BASE_DIR = obter_base_path()

DATA_DIR = BASE_DIR / "data"
PEDIDOS_DIR = BASE_DIR / "pedidos_txt"
CUPONS_DIR = BASE_DIR / "cupons_formatados"
BACKUP_DIR = BASE_DIR / "backups"
CONFIG_DIR = BASE_DIR / "config"


PASTAS = [
    BASE_DIR,
    DATA_DIR,
    PEDIDOS_DIR,
    CUPONS_DIR,
    BACKUP_DIR,
    CONFIG_DIR
]

for pasta in PASTAS:
    pasta.mkdir(exist_ok=True)