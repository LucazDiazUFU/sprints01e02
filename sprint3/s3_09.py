import json
import numpy as np

from trabalho2.risco import AnaliseRisco
from .cenario import criar_cenario


def analisar():
    inventario = criar_cenario()
    resultado = AnaliseRisco().calcular(inventario)
    matriz = np.array(resultado["M"])
    vetor = np.array(resultado["v"])
    fatores = np.diag([ativo.fator_exposicao() for ativo in inventario.listar_ativos()])
    _, _, transposta = np.linalg.svd(matriz)
    posto = int(np.linalg.matrix_rank(matriz))
    nucleo = transposta[posto:].T
    vetor_plano = np.array([2.0, 1.0])
    rotacao = np.array([[0.0, -1.0], [1.0, 0.0]])
    reflexao = np.diag([1.0, -1.0])
    escala = np.diag([2.0, 3.0])
    return {
        "M": matriz.tolist(),
        "v": vetor.tolist(),
        "b": (matriz @ vetor).tolist(),
        "dimensoes": {"entrada": 4, "saida": 3},
        "posto": posto,
        "base_nucleo": nucleo.tolist(),
        "teste_nucleo": np.allclose(matriz @ nucleo, 0),
        "F": fatores.tolist(),
        "F_M_v": (fatores @ (matriz @ vetor)).tolist(),
        "FM_v": ((fatores @ matriz) @ vetor).tolist(),
        "rotacao": (rotacao @ vetor_plano).tolist(),
        "reflexao": (reflexao @ vetor_plano).tolist(),
        "escala": (escala @ vetor_plano).tolist(),
        "composicao": (escala @ rotacao @ vetor_plano).tolist(),
        "linearidade": np.allclose(
            matriz @ (vetor + vetor), matriz @ vetor + matriz @ vetor
        ),
        "quadrado_nao_linear": {"T_2_3": (2 + 3) ** 2, "T_2_mais_T_3": 2**2 + 3**2},
    }


if __name__ == "__main__":
    print(json.dumps(analisar(), ensure_ascii=False, indent=2))
