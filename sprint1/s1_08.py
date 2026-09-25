ativos = ["Servidor", "Notebook"]

for numero in range(1, 11):
    print(numero)

while True:
    print("\n1 - Cadastrar ativo")
    print("2 - Listar ativos")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        nome = input("Digite o nome do ativo: ").strip()
        if not nome:
            print("O nome não pode ficar vazio.")
            continue
        ativos.append(nome)
        print("Ativo cadastrado.")
    elif opcao == "2":
        for posicao, nome in enumerate(ativos, start=1):
            print(f"{posicao} - {nome}")
    elif opcao == "0":
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida.")
