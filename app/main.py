from services import (
    adicionar_cliente,
    listar_clientes,
    adicionar_produto,
    listar_produtos,
    criar_pedido,
    listar_pedidos,
    fechamento_do_dia
)

def menu():
    print("\n=== PedidoFlow ===")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Cadastrar produto")
    print("4 - Listar produtos")
    print("5 - Criar pedido")
    print("6 - Listar pedidos")
    print("7 - Fechamento do dia")
    print("0 - Sair")


while True:
    menu()
    opcao = input("Escolha: ")

    if opcao == "1":
        nome = input("Nome: ")
        telefone = input("Telefone: ")
        endereco = input("Endereço: ")
        bairro = input("Bairro: ")
        obs = input("Observações: ")

        adicionar_cliente(nome, telefone, endereco, bairro, obs)
        print("Cliente cadastrado com sucesso!")

    elif opcao == "2":
        clientes = listar_clientes()
        for c in clientes:
            print(f"\nID: {c[0]} | Nome: {c[1]} | Bairro: {c[4]}")

    elif opcao == "3":
        nome = input("Nome do produto: ")
        categoria = input("Categoria: ")
        tamanho = input("Tamanho: ")
        preco = float(input("Preço: ").replace(",", "."))

        adicionar_produto(nome, categoria, tamanho, preco)
        print("Produto cadastrado com sucesso!")

    elif opcao == "4":
        produtos = listar_produtos()
        for p in produtos:
            print(f"\nID: {p[0]} | Nome: {p[1]} | R$ {p[4]:.2f}")

    elif opcao == "5":
        print("\nClientes:")
        clientes = listar_clientes()
        for c in clientes:
            print(f"{c[0]} - {c[1]} | Bairro: {c[4]}")

        cliente_id = int(input("\nID do cliente: "))

        itens = []

        while True:
            print("\nProdutos:")
            produtos = listar_produtos()
            for p in produtos:
                print(f"{p[0]} - {p[1]} | R$ {p[4]:.2f}")

            produto_id = int(input("\nID do produto: "))
            quantidade = int(input("Quantidade: "))

            itens.append({
                "produto_id": produto_id,
                "quantidade": quantidade
            })

            if input("Adicionar mais? (s/n): ").lower() != "s":
                break

        pedido_id, msg = criar_pedido(cliente_id, itens)

        if pedido_id:
            print(f"Pedido #{pedido_id} criado!")
        else:
            print(msg)

    elif opcao == "6":
        pedidos = listar_pedidos()
        for p in pedidos:
            print(f"\nPedido {p[0]} | Cliente: {p[1]} | Total: R$ {p[5]:.2f}")

    elif opcao == "7":
        dados = fechamento_do_dia()

        print("\n=== FECHAMENTO DO DIA ===")
        print(f"Total vendido: R$ {dados['total_vendido']:.2f}")
        print(f"Total de pedidos: {dados['total_pedidos']}")
        print(f"Total entrega: R$ {dados['total_entrega']:.2f}")
        print(f"Cancelados: {dados['cancelados']}")
        print(f"Mais vendido: {dados['mais_vendido']}")

    elif opcao == "0":
        break

    else:
        print("Opção inválida!")