import json
import numpy as np

from trabalho2.risco import AnaliseRisco
from .cenario import criar_cenario


def escalonar(matriz, vetor, tolerancia=1e-10):
    matriz = np.asarray(matriz, dtype=float)
    vetor = np.asarray(vetor, dtype=float)
    if matriz.ndim != 2 or vetor.shape != (matriz.shape[0],):
        raise ValueError("Dimensões incompatíveis.")
    aumentada = np.column_stack([matriz, vetor])
    linhas, colunas = matriz.shape
    linha = 0
    etapas = [aumentada.tolist()]
    for coluna in range(colunas):
        if linha == linhas:
            break
        pivo = linha + int(np.argmax(np.abs(aumentada[linha:, coluna])))
        if abs(aumentada[pivo, coluna]) <= tolerancia:
            continue
        aumentada[[linha, pivo]] = aumentada[[pivo, linha]]
        aumentada[linha] /= aumentada[linha, coluna]
        for i in range(linha + 1, linhas):
            aumentada[i] -= aumentada[i, coluna] * aumentada[linha]
        etapas.append(aumentada.tolist())
        linha += 1
    for i in range(linhas):
        if (
            np.all(np.abs(aumentada[i, :-1]) <= tolerancia)
            and abs(aumentada[i, -1]) > tolerancia
        ):
            return {"classificacao": "SI", "solucao": None, "etapas": etapas}
    if linha < colunas:
        return {"classificacao": "SPI", "solucao": None, "etapas": etapas}
    solucao = np.zeros(colunas)
    for i in range(colunas - 1, -1, -1):
        solucao[i] = (
            aumentada[i, -1] - aumentada[i, i + 1 : colunas] @ solucao[i + 1 :]
        ) / aumentada[i, i]
    return {"classificacao": "SPD", "solucao": solucao.tolist(), "etapas": etapas}


def demonstrar():
    risco = AnaliseRisco().calcular(criar_cenario())
    sistema = np.eye(3) - np.array(risco["A"])
    vetor = np.array([item["risco_proprio"] for item in risco["ativos"]])
    print(
        json.dumps(
            {
                "sistema_2": escalonar([[1, 1], [2, 1]], [3, 4]),
                "sistema_3": escalonar(
                    [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]
                ),
                "infinitas": escalonar([[1, 1], [2, 2]], [3, 6]),
                "impossivel": escalonar([[1, 1], [2, 2]], [3, 7]),
                "risco": escalonar(sistema, vetor),
                "numpy": np.linalg.solve(sistema, vetor).tolist(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    demonstrar()
