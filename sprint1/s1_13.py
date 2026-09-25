from enum import Enum


class StatusAtivo(Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"
    EM_MANUTENCAO = "Em manutenção"


class Severidade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    CRITICA = "Crítica"


id_ativo = input("ID do ativo: ").strip()
nome = input("Nome do ativo: ").strip()
print("Status disponíveis:")
for numero, status in enumerate(StatusAtivo, 1):
    print(f"{numero} - {status.value}")

opcao = input("Escolha o status: ")
if not id_ativo or not nome:
    print("ID e nome são obrigatórios.")
elif opcao not in {"1", "2", "3"}:
    print("Status inválido.")
else:
    status = list(StatusAtivo)[int(opcao) - 1]
    print(f"ID: {id_ativo} | Ativo: {nome} | Status: {status.value}")
