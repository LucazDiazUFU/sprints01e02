import json
from pathlib import Path


arquivo = Path(__file__).with_name("ativos.json")


class DadosInvalidosError(ValueError):
    pass


def carregar_ativos():
    try:
        with arquivo.open("r", encoding="utf-8") as entrada:
            dados = json.load(entrada)
        if not isinstance(dados, list):
            raise DadosInvalidosError("O formato do arquivo é inválido.")
        return dados
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError, DadosInvalidosError) as erro:
        print(f"Não foi possível carregar os ativos: {erro}")
        raise SystemExit(1)


def salvar_ativos(ativos):
    temporario = arquivo.with_suffix(".tmp")
    try:
        with temporario.open("w", encoding="utf-8") as saida:
            json.dump(ativos, saida, ensure_ascii=False, indent=2)
        temporario.replace(arquivo)
        return True
    except OSError:
        print("Não foi possível salvar os ativos.")
        return False


def cadastrar_ativo(ativos, identificador, nome, responsavel):
    if not identificador or not nome or not responsavel:
        raise DadosInvalidosError("ID, nome e responsável são obrigatórios.")
    if any(ativo["id"] == identificador for ativo in ativos):
        raise DadosInvalidosError("Esse ID já foi cadastrado.")
    novo = {"id": identificador, "nome": nome, "responsavel": responsavel}
    ativos.append(novo)
    if salvar_ativos(ativos):
        print("Ativo cadastrado.")
    else:
        ativos.pop()


ativos = carregar_ativos()
while True:
    print("\n1 - Cadastrar ativo")
    print("2 - Listar ativos")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        try:
            cadastrar_ativo(
                ativos,
                input("ID do ativo: ").strip(),
                input("Nome do ativo: ").strip(),
                input("Responsável: ").strip(),
            )
        except DadosInvalidosError as erro:
            print(erro)
    elif opcao == "2":
        if not ativos:
            print("Nenhum ativo cadastrado.")
        for ativo in ativos:
            print(f"ID: {ativo['id']} | Nome: {ativo['nome']} | Responsável: {ativo['responsavel']}")
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")
