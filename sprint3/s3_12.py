import json
import math
import numpy as np


def erros(aproximado, referencia):
    absoluto = abs(aproximado - referencia)
    return {
        "absoluto": absoluto,
        "relativo": absoluto / abs(referencia) if referencia else None,
    }


def experimentar():
    matriz = np.array([[1.0, 1.0], [1.0, 1.0 + 1e-10]])
    vetor = np.array([2.0, 2.0 + 1e-10])
    direta = np.linalg.solve(matriz, vetor)
    inversa = np.linalg.inv(matriz) @ vetor
    alterada = np.linalg.solve(matriz, vetor + np.array([0, 1e-8]))
    return {
        "soma": 0.1 + 0.2,
        "igualdade": 0.1 + 0.2 == 0.3,
        "com_tolerancia": math.isclose(0.1 + 0.2, 0.3),
        "truncado": math.trunc(math.pi * 1000) / 1000,
        "arredondado": round(math.pi, 3),
        "erro_truncamento": erros(math.trunc(math.pi * 1000) / 1000, math.pi),
        "erro_arredondamento": erros(round(math.pi, 3), math.pi),
        "dez_somas": sum([0.1] * 10),
        "erro_propagado": erros(sum([0.1] * 10), 1),
        "determinante": float(np.linalg.det(matriz)),
        "condicao": float(np.linalg.cond(matriz)),
        "solve": direta.tolist(),
        "inv": inversa.tolist(),
        "solve_perturbado": alterada.tolist(),
        "residuo_solve": float(np.linalg.norm(matriz @ direta - vetor)),
        "residuo_inv": float(np.linalg.norm(matriz @ inversa - vetor)),
    }


if __name__ == "__main__":
    print(json.dumps(experimentar(), ensure_ascii=False, indent=2))
