from dataclasses import dataclass, field
import math

from trabalho1.modelos import Ativo, Vulnerabilidade
from trabalho1.validacoes import numero, tipo_ativo


@dataclass
class Equipamento(Ativo):
    dependencias: dict[int, float] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.dependencias, dict):
            raise ValueError("Dependências devem relacionar ID e peso.")
        dependencias = {}
        for id_ativo, peso in self.dependencias.items():
            id_ativo = numero(id_ativo, "ID da dependência")
            if id_ativo == self.id:
                raise ValueError("Um ativo não pode depender de si mesmo.")
            if isinstance(peso, bool):
                raise ValueError(
                    "O peso deve ser um número entre 0 e 1, sem incluir 1."
                )
            try:
                peso = float(peso)
            except (TypeError, ValueError) as erro:
                raise ValueError("O peso deve ser um número entre 0 e 1.") from erro
            if not math.isfinite(peso) or not 0 <= peso < 1:
                raise ValueError("O peso deve estar entre 0 e 1, sem incluir 1.")
            if id_ativo in dependencias:
                raise ValueError("ID de dependência duplicado.")
            dependencias[id_ativo] = peso
        if sum(dependencias.values()) >= 1:
            raise ValueError("A soma dos pesos de cada ativo deve ser menor que 1.")
        self.dependencias = dependencias

    def fator_exposicao(self):
        return 1.0

    def exibir_detalhes(self):
        return f"Ativo {self.id}: {self.nome} | {self.responsavel} | {self.setor}"

    @classmethod
    def carregar(cls, dados):
        return criar_equipamento(dados)


class Notebook(Equipamento):
    def exibir_detalhes(self):
        return f"Notebook | {super().exibir_detalhes()}"


class Servidor(Equipamento):
    def fator_exposicao(self):
        return 1.2

    def exibir_detalhes(self):
        return f"Servidor | {super().exibir_detalhes()}"


class Roteador(Equipamento):
    def fator_exposicao(self):
        return 1.1

    def exibir_detalhes(self):
        return f"Roteador | {super().exibir_detalhes()}"


def criar_equipamento(dados):
    if not isinstance(dados, dict):
        raise ValueError("Cada ativo precisa ser um objeto JSON.")
    dados = dados.copy()
    obrigatorios = {"id", "nome", "responsavel", "setor", "tipo"}
    permitidos = obrigatorios | {
        "criticidade",
        "status",
        "descricao",
        "vulnerabilidades",
        "dependencias",
    }
    if not obrigatorios <= dados.keys() or not dados.keys() <= permitidos:
        raise ValueError("Campos obrigatórios ausentes ou campos desconhecidos.")
    dados["tipo"] = tipo_ativo(dados["tipo"])
    vulnerabilidades = dados.get("vulnerabilidades", [])
    if not isinstance(vulnerabilidades, list):
        raise ValueError("Vulnerabilidades devem ser uma lista.")
    try:
        dados["vulnerabilidades"] = [
            item if isinstance(item, Vulnerabilidade) else Vulnerabilidade(**item)
            for item in vulnerabilidades
        ]
    except TypeError as erro:
        raise ValueError("Campos de vulnerabilidade inválidos.") from erro
    classe = {1: Notebook, 2: Servidor, 3: Roteador}.get(dados["tipo"], Equipamento)
    return classe(**dados)
