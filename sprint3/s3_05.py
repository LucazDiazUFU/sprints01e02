import json


def bubble_sort(itens, chave=lambda valor: valor):
    itens = list(itens)
    comparacoes = 0
    for fim in range(len(itens) - 1, 0, -1):
        mudou = False
        for i in range(fim):
            comparacoes += 1
            if chave(itens[i]) > chave(itens[i + 1]):
                itens[i], itens[i + 1] = itens[i + 1], itens[i]
                mudou = True
        if not mudou:
            break
    return itens, comparacoes


def selection_sort(itens, chave=lambda valor: valor):
    itens = list(itens)
    comparacoes = 0
    for i in range(len(itens) - 1):
        menor = i
        for j in range(i + 1, len(itens)):
            comparacoes += 1
            if chave(itens[j]) < chave(itens[menor]):
                menor = j
        itens[i], itens[menor] = itens[menor], itens[i]
    return itens, comparacoes


def insertion_sort(itens, chave=lambda valor: valor):
    itens = list(itens)
    comparacoes = 0
    for i in range(1, len(itens)):
        atual = itens[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if chave(itens[j]) <= chave(atual):
                break
            itens[j + 1] = itens[j]
            j -= 1
        itens[j + 1] = atual
    return itens, comparacoes


def busca_binaria(itens, valor, chave=lambda item: item):
    inicio, fim = 0, len(itens) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        atual = chave(itens[meio])
        if atual == valor:
            return meio, comparacoes
        if atual < valor:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None, comparacoes


def comparar():
    tabela = []
    for tamanho in (10, 50, 100):
        dados = list(range(tamanho, 0, -1))
        linha = {"tamanho": tamanho}
        for ordenar in (bubble_sort, selection_sort, insertion_sort):
            ordenados, comparacoes = ordenar(dados)
            linha[ordenar.__name__] = comparacoes
            if ordenados != sorted(dados):
                raise RuntimeError("A ordenação produziu resultado incorreto.")
        linha["busca_binaria"] = busca_binaria(sorted(dados), tamanho)[1]
        tabela.append(linha)
    return tabela


def demonstrar():
    ativos = [
        {"id": 103, "nome": "roteador-01"},
        {"id": 101, "nome": "notebook-01"},
        {"id": 102, "nome": "servidor-01"},
    ]
    ordenados, _ = insertion_sort(ativos, chave=lambda ativo: ativo["id"])
    print(
        json.dumps(
            {
                "ativos": ordenados,
                "busca_102": busca_binaria(
                    ordenados, 102, chave=lambda ativo: ativo["id"]
                ),
                "comparacoes": comparar(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    demonstrar()
