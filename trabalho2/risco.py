import numpy as np


class AnaliseRisco:
    severidades = {"BAIXA": 2.0, "MEDIA": 5.0, "ALTA": 8.0, "CRITICA": 10.0}

    @staticmethod
    def resolver(matriz, risco_proprio):
        matriz = np.asarray(matriz, dtype=float)
        risco_proprio = np.asarray(risco_proprio, dtype=float)
        n = len(risco_proprio)
        if matriz.shape != (n, n) or risco_proprio.shape != (n,):
            raise ValueError("Dimensões incompatíveis para o sistema linear.")
        if not np.isfinite(matriz).all() or not np.isfinite(risco_proprio).all():
            raise ValueError("O sistema contém valores não finitos.")
        if n == 0:
            return np.array([]), 1.0, 1.0, 0.0
        determinante = float(np.linalg.det(matriz))
        condicao = float(np.linalg.cond(matriz))
        if np.linalg.matrix_rank(matriz) < n or not np.isfinite(condicao):
            raise ValueError(
                "I - A não é invertível; o risco efetivo não foi calculado."
            )
        try:
            risco_efetivo = np.linalg.solve(matriz, risco_proprio)
        except np.linalg.LinAlgError as erro:
            raise ValueError("Não foi possível resolver o sistema linear.") from erro
        if not np.isfinite(risco_efetivo).all():
            raise ValueError("A solução não contém valores finitos.")
        residuo = float(np.linalg.norm(matriz @ risco_efetivo - risco_proprio))
        return risco_efetivo, determinante, condicao, residuo

    def calcular(self, inventario, ponderar=False):
        ativos = inventario.listar_ativos()
        ids = [ativo.id for ativo in ativos]
        vulnerabilidades = sorted(
            (item for ativo in ativos for item in ativo.vulnerabilidades),
            key=lambda item: item.id,
        )
        ids_vulnerabilidades = [item.id for item in vulnerabilidades]
        indice_ativos = {id_ativo: i for i, id_ativo in enumerate(ids)}
        indice_vulnerabilidades = {
            id_vulnerabilidade: j
            for j, id_vulnerabilidade in enumerate(ids_vulnerabilidades)
        }
        matriz = np.zeros((len(ativos), len(vulnerabilidades)))
        dependencias = np.zeros((len(ativos), len(ativos)))
        severidades = np.array(
            [
                (
                    item.cvss
                    if item.cvss is not None
                    else self.severidades[item.severidade]
                )
                for item in vulnerabilidades
            ]
        )
        inventario.validar_dependencias()
        for i, ativo in enumerate(ativos):
            for item in ativo.vulnerabilidades:
                matriz[i, indice_vulnerabilidades[item.id]] = 1
            for id_ativo, peso in ativo.dependencias.items():
                dependencias[i, indice_ativos[id_ativo]] = peso
        fatores = np.array(
            [ativo.fator_exposicao() if ponderar else 1.0 for ativo in ativos]
        )
        risco_proprio = fatores * (matriz @ severidades)
        sistema = np.eye(len(ativos)) - dependencias
        efetivo, determinante, condicao, residuo = self.resolver(sistema, risco_proprio)
        return {
            "ativos": [
                {
                    "id": ativo.id,
                    "nome": ativo.nome,
                    "risco_proprio": float(risco_proprio[i]),
                    "risco_efetivo": float(efetivo[i]),
                    "fator_exposicao": float(fatores[i]),
                }
                for i, ativo in enumerate(ativos)
            ],
            "ids_ativos": ids,
            "ids_vulnerabilidades": ids_vulnerabilidades,
            "M": matriz.tolist(),
            "v": severidades.tolist(),
            "A": dependencias.tolist(),
            "determinante": determinante,
            "condicao": condicao,
            "residuo": residuo,
            "aviso": (
                "Matriz mal condicionada; confira a precisão." if condicao > 1e8 else ""
            ),
            "ponderado": ponderar,
        }
