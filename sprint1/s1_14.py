import json
from pathlib import Path


arquivo = Path(__file__).with_name("vulnerabilidades.json")

try:
    with arquivo.open("r", encoding="utf-8") as entrada:
        vulnerabilidades = json.load(entrada)
    if not isinstance(vulnerabilidades, list):
        print("O arquivo de dados está inválido.")
        raise SystemExit(1)
except FileNotFoundError:
    vulnerabilidades = []
except (OSError, json.JSONDecodeError):
    print("Não foi possível ler os dados. O arquivo original não será alterado.")
    raise SystemExit(1)

while True:
    print("\n1 - Cadastrar vulnerabilidade")
    print("2 - Listar vulnerabilidades")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        identificador = input("ID: ").strip()
        descricao = input("Descrição: ").strip()
        id_ativo = input("ID do ativo: ").strip()
        try:
            grau = int(input("Grau da vulnerabilidade (0 a 10): "))
        except ValueError:
            print("Digite um número inteiro para o grau.")
            continue

        if not identificador or not descricao or not id_ativo:
            print("Todos os campos são obrigatórios.")
        elif not 0 <= grau <= 10:
            print("O grau deve estar entre 0 e 10.")
        elif any(item["id"] == identificador for item in vulnerabilidades):
            print("Esse ID já foi cadastrado.")
        else:
            novo = {"id": identificador, "descricao": descricao, "id_ativo": id_ativo, "grau": grau}
            vulnerabilidades.append(novo)
            try:
                with arquivo.open("w", encoding="utf-8") as saida:
                    json.dump(vulnerabilidades, saida, ensure_ascii=False, indent=2)
                print("Vulnerabilidade cadastrada e salva.")
            except OSError:
                vulnerabilidades.pop()
                print("Não foi possível gravar o arquivo.")
    elif opcao == "2":
        if not vulnerabilidades:
            print("Nenhuma vulnerabilidade cadastrada.")
        for item in vulnerabilidades:
            print(f"ID: {item['id']} | Ativo: {item['id_ativo']} | Grau: {item['grau']} | {item['descricao']}")
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")
