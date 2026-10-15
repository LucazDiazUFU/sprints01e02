import json
import numpy as np

from trabalho2.risco import AnaliseRisco


def determinante_sarrus(matriz):
    matriz = np.asarray(matriz, dtype=float)
    if matriz.shape != (3, 3):
        raise ValueError("Sarrus é usado apenas em matrizes 3 por 3.")
    a, b, c = matriz[0]
    d, e, f = matriz[1]
    g, h, i = matriz[2]
    return float(a * e * i + b * f * g + c * d * h - c * e * g - b * d * i - a * f * h)


def determinante_cofatores(matriz):
    matriz = np.asarray(matriz, dtype=float)
    if matriz.ndim != 2 or matriz.shape[0] != matriz.shape[1]:
        raise ValueError("A matriz precisa ser quadrada.")
    if len(matriz) == 0:
        return 1.0
    if len(matriz) == 1:
        return float(matriz[0, 0])
    return sum(
        (-1) ** j
        * matriz[0, j]
        * determinante_cofatores(np.delete(np.delete(matriz, 0, axis=0), j, axis=1))
        for j in range(len(matriz))
    )


if __name__ == "__main__":
    matriz2 = np.array([[2.0, 1.0], [1.0, 1.0]])
    matriz3 = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])
    dependencia_singular = np.full((3, 3), 0.5)
    np.fill_diagonal(dependencia_singular, 0)
    sistema_singular = np.eye(3) - dependencia_singular
    try:
        AnaliseRisco.resolver(sistema_singular, [10, 8, 2])
        singular = False
    except ValueError:
        singular = True
    print(
        json.dumps(
            {
                "det_2": float(np.linalg.det(matriz2)),
                "inversa_2": np.linalg.inv(matriz2).tolist(),
                "produto": (matriz2 @ np.linalg.inv(matriz2)).tolist(),
                "sarrus": determinante_sarrus(matriz3),
                "cofatores": determinante_cofatores(matriz3),
                "numpy": float(np.linalg.det(matriz3)),
                "A_singular": dependencia_singular.tolist(),
                "det_I_A": float(np.linalg.det(sistema_singular)),
                "singular_rejeitado": singular,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
