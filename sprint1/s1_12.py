ativo = {
    "nome": "Notebook administrativo",
    "ip": "192.168.1.10",
    "sistema_operacional": "Windows",
    "criticidade": "Média",
    "vulnerabilidades": {}
}

while True:
    print("\n1 - Cadastrar vulnerabilidade")
    print("2 - Atualizar vulnerabilidade")
    print("3 - Listar vulnerabilidades")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        identificador = input("ID da vulnerabilidade: ").strip()
        descricao = input("Descrição: ").strip()
        if identificador == "" or descricao == "":
            print("ID e descrição são obrigatórios.")
        elif identificador in ativo["vulnerabilidades"]:
            print("Esse ID já foi cadastrado.")
        else:
            ativo["vulnerabilidades"][identificador] = descricao
            print("Vulnerabilidade cadastrada.")
    elif opcao == "2":
        identificador = input("ID da vulnerabilidade: ").strip()
        if identificador in ativo["vulnerabilidades"]:
            descricao = input("Nova descrição: ").strip()
            if descricao == "":
                print("A descrição não pode ficar vazia.")
            else:
                ativo["vulnerabilidades"][identificador] = descricao
                print("Vulnerabilidade atualizada.")
        else:
            print("Vulnerabilidade não encontrada.")
    elif opcao == "3":
        print(f"Ativo: {ativo['nome']}")
        for chave, valor in ativo.items():
            if chave != "vulnerabilidades":
                print(f"{chave}: {valor}")
        if not ativo["vulnerabilidades"]:
            print("Nenhuma vulnerabilidade cadastrada.")
        for identificador, descricao in ativo["vulnerabilidades"].items():
            print(f"ID: {identificador} | Descrição: {descricao}")
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")
