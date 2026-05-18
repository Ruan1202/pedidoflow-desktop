import json
from paths import CONFIG_DIR

APP_NAME = "PedidoFlow"

ARQUIVO_TEMA = CONFIG_DIR / "tema.json"

TEMA_PADRAO = {
    "appearance": "dark",
    "primary": "#2563EB"
}

CORES_FIXAS = {
    "bg": "#0F172A",
    "sidebar": "#111827",
    "card": "#1E293B",
    "card_hover": "#334155",
    "danger": "#DC2626",
    "danger_hover": "#B91C1C",
    "success": "#16A34A",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
}


def carregar_tema():
    if not ARQUIVO_TEMA.exists():
        salvar_tema(TEMA_PADRAO)
        return TEMA_PADRAO

    try:
        with open(ARQUIVO_TEMA, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except:
        salvar_tema(TEMA_PADRAO)
        return TEMA_PADRAO


def salvar_tema(dados):
    with open(ARQUIVO_TEMA, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


TEMA = carregar_tema()

COLORS = {
    **CORES_FIXAS,
    "primary": TEMA.get("primary", "#2563EB"),
    "primary_hover": TEMA.get("primary", "#2563EB"),
}

FONTS = {
    "title": ("Arial", 26, "bold"),
    "subtitle": ("Arial", 18, "bold"),
    "normal": ("Arial", 14),
    "small": ("Arial", 12),
    "button": ("Arial", 14, "bold"),
}


def aplicar_tema(ctk):
    aparencia = TEMA.get("appearance", "dark")
    ctk.set_appearance_mode(aparencia)
    ctk.set_default_color_theme("blue")