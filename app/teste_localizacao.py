from localizacao import calcular_entrega_por_endereco

endereco = input("Digite o endereço do cliente: ")

distancia, taxa, mensagem = calcular_entrega_por_endereco(endereco)

print("\nResultado:")
print(mensagem)

if distancia is not None:
    print(f"Distância: {distancia:.2f} km")

if taxa is not None:
    print(f"Taxa: R$ {taxa:.2f}")