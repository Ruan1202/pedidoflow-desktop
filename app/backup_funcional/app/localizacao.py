from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from database import conectar


def buscar_configuracao_loja():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome_loja, endereco_loja, latitude, longitude
        FROM configuracoes_loja
        LIMIT 1
    """)

    dados = cursor.fetchone()

    conn.close()

    return dados


def buscar_taxas_distancia():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT distancia_km, valor
        FROM taxas_distancia
        ORDER BY distancia_km ASC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def geocodificar_endereco(endereco):
    geolocator = Nominatim(user_agent="crm_atendimento_delivery")

    local = geolocator.geocode(endereco)

    if not local:
        return None

    return local.latitude, local.longitude


def calcular_distancia_km(lat_origem, lon_origem, lat_destino, lon_destino):
    origem = (lat_origem, lon_origem)
    destino = (lat_destino, lon_destino)

    return geodesic(origem, destino).km


def calcular_taxa_por_distancia(distancia_km):
    taxas = buscar_taxas_distancia()

    for limite_km, valor in taxas:
        if distancia_km <= limite_km:
            return valor

    return None


def calcular_entrega_por_endereco(endereco_cliente):
    loja = buscar_configuracao_loja()

    if not loja:
        return None, None, "Configuração da loja não encontrada."

    nome_loja, endereco_loja, lat_loja, lon_loja = loja

    if lat_loja is None or lon_loja is None:
        return None, None, "Latitude/longitude da loja não configuradas."

    coordenadas_cliente = geocodificar_endereco(endereco_cliente)

    if not coordenadas_cliente:
        return None, None, "Endereço do cliente não encontrado."

    lat_cliente, lon_cliente = coordenadas_cliente

    distancia = calcular_distancia_km(
        lat_loja,
        lon_loja,
        lat_cliente,
        lon_cliente
    )

    taxa = calcular_taxa_por_distancia(distancia)

    if taxa is None:
        return distancia, None, "Endereço fora da área de entrega."

    return distancia, taxa, "Taxa calculada com sucesso."