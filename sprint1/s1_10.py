ativos = []

while True:
    print("\n1 - Cadastrar ativo")
    print("2 - Remover ativo")
    print("3 - Listar ativos")
    print("4 - Buscar ativo")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome do ativo: ").strip()
        if nome == "":
            print("O nome não pode ficar vazio.")
        elif nome in ativos:
            print("Esse ativo já está cadastrado.")
        else:
            ativos.append(nome)
            print("Ativo cadastrado.")
    elif opcao == "2":
        nome = input("Nome do ativo que deseja remover: ").strip()
        if nome in ativos:
            ativos.remove(nome)
            print("Ativo removido.")
        else:
            print("Ativo não encontrado.")
    elif opcao == "3":
        if len(ativos) == 0:
            print("Nenhum ativo cadastrado.")
        else:
            for numero, nome in enumerate(ativos, 1):
                print(f"{numero} - {nome}")
    elif opcao == "4":
        nome = input("Nome do ativo: ").strip()
        if nome in ativos:
            print(f"O ativo {nome} está cadastrado.")
        else:
            print("Ativo não encontrado.")
    elif opcao == "0":
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida.")
