from datetime import datetime
import os


LARGURA_CUPOM = 42


def linha():
    return "-" * LARGURA_CUPOM


def centralizar(texto):
    return texto.center(LARGURA_CUPOM)


def formatar_cupom(texto_pedido):
    linhas = []

    linhas.append(centralizar("CRM ATENDIMENTO"))
    linhas.append(centralizar("COMPROVANTE DE PEDIDO"))
    linhas.append(linha())
    linhas.append(datetime.now().strftime("%d/%m/%Y %H:%M").center(LARGURA_CUPOM))
    linhas.append(linha())

    for linha_texto in texto_pedido.split("\n"):
        linhas.append(linha_texto)

    linhas.append(linha())
    linhas.append(centralizar("Obrigado pela preferência!"))
    linhas.append("\n\n")

    return "\n".join(linhas)


def salvar_cupom_formatado(texto_pedido, pedido_id):
    pasta = "cupons_formatados"
    os.makedirs(pasta, exist_ok=True)

    cupom = formatar_cupom(texto_pedido)

    caminho = os.path.join(pasta, f"cupom_{pedido_id}.txt")

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(cupom)

    return caminho


def simular_impressao(texto_pedido, pedido_id):
    caminho = salvar_cupom_formatado(texto_pedido, pedido_id)
    return caminho