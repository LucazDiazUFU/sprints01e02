import json
from .s3_05 import busca_binaria


def busca_linear(itens, valor):
    for comparacoes, item in enumerate(itens, 1):
        if item == valor:
            return comparacoes
    return len(itens)


def demonstrar():
    tabela = []
    for tamanho in (10, 100, 1000):
        itens = list(range(tamanho))
        tabela.append(
            {
                "n": tamanho,
                "linear": busca_linear(itens, tamanho - 1),
                "binaria": busca_binaria(itens, tamanho - 1)[1],
                "duplo_laco": sum(1 for _ in itens for _ in itens),
            }
        )
    print(json.dumps(tabela, indent=2))


if __name__ == "__main__":
    demonstrar()
