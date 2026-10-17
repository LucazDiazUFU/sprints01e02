from functools import lru_cache, reduce
import json
from time import perf_counter


def validar_numero(numero):
    if isinstance(numero, bool) or not isinstance(numero, int) or numero < 0:
        raise ValueError("Informe um inteiro não negativo.")


def fatorial_iterativo(numero):
    validar_numero(numero)
    resultado = 1
    for valor in range(2, numero + 1):
        resultado *= valor
    return resultado


def fatorial_recursivo(numero):
    validar_numero(numero)
    if numero > 900:
        raise ValueError("Use a versão iterativa para entradas maiores que 900.")
    if numero <= 1:
        return 1
    return numero * fatorial_recursivo(numero - 1)


def fibonacci(numero):
    validar_numero(numero)
    if numero > 35:
        raise ValueError("Use a versão com memoização para entradas maiores que 35.")
    if numero < 2:
        return numero
    return fibonacci(numero - 1) + fibonacci(numero - 2)


@lru_cache(maxsize=None)
def fibonacci_memorizado(numero):
    validar_numero(numero)
    if numero > 400:
        raise ValueError("O exemplo recursivo aceita até 400.")
    if numero < 2:
        return numero
    return fibonacci_memorizado(numero - 1) + fibonacci_memorizado(numero - 2)


def medir(funcao, numero):
    inicio = perf_counter()
    resultado = funcao(numero)
    return {"resultado": resultado, "segundos": perf_counter() - inicio}


def demonstrar():
    fibonacci_memorizado.cache_clear()
    ativos = [
        {"id": 103, "nome": "roteador-01", "tipo": 3},
        {"id": 101, "nome": "notebook-01", "tipo": 1},
        {"id": 102, "nome": "servidor-01", "tipo": 2},
    ]
    print(
        json.dumps(
            {
                "fatorial_iterativo": medir(fatorial_iterativo, 15),
                "fatorial_recursivo": medir(fatorial_recursivo, 15),
                "fibonacci": medir(fibonacci, 25),
                "fibonacci_memorizado": medir(fibonacci_memorizado, 25),
                "nomes": list(map(lambda ativo: ativo["nome"].upper(), ativos)),
                "servidores": list(filter(lambda ativo: ativo["tipo"] == 2, ativos)),
                "ordenados": sorted(ativos, key=lambda ativo: ativo["id"]),
                "soma_ids": reduce(lambda total, ativo: total + ativo["id"], ativos, 0),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    demonstrar()
