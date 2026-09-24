from dataclasses import dataclass, field

from .validacoes import (
    CRITICIDADES, SEVERIDADES, STATUS_ATIVO, STATUS_VULNERABILIDADE,
    cve, cvss, numero, opcao, texto, tipo_ativo,
)


@dataclass
class Vulnerabilidade:
    id: int
    descricao: str
    categoria: str
    severidade: str
    status: str
    cve: str = ""
    cvss: float | None = None
    referencia: str = ""
    recomendacao: str = ""

    def __post_init__(self):
        self.id = numero(self.id, "ID da vulnerabilidade")
        self.descricao = texto(self.descricao, "Descrição", 500)
        self.categoria = texto(self.categoria, "Categoria")
        self.severidade = opcao(self.severidade, SEVERIDADES, "Severidade")
        self.status = opcao(self.status, STATUS_VULNERABILIDADE, "Status")
        self.cve = cve(self.cve)
        self.cvss = cvss(self.cvss)
        self.referencia = str(self.referencia or "").strip()
        self.recomendacao = str(self.recomendacao or "").strip()

    def dados(self):
        return vars(self).copy()


@dataclass
class Ativo:
    id: int
    nome: str
    responsavel: str
    setor: str
    tipo: int
    criticidade: str = "MEDIA"
    status: str = "ATIVO"
    descricao: str = ""
    vulnerabilidades: list[Vulnerabilidade] = field(default_factory=list)

    def __post_init__(self):
        self.id = numero(self.id, "ID do ativo")
        self.nome = texto(self.nome, "Nome")
        self.responsavel = texto(self.responsavel, "Responsável")
        self.setor = texto(self.setor, "Setor")
        self.tipo = tipo_ativo(self.tipo)
        self.criticidade = opcao(self.criticidade, CRITICIDADES, "Criticidade")
        self.status = opcao(self.status, STATUS_ATIVO, "Status")
        self.descricao = str(self.descricao or "").strip()

    def dados(self):
        dados = vars(self).copy()
        dados["vulnerabilidades"] = [item.dados() for item in self.vulnerabilidades]
        return dados

    @classmethod
    def carregar(cls, dados):
        dados = dados.copy()
        dados["vulnerabilidades"] = [Vulnerabilidade(**item) for item in dados.get("vulnerabilidades", [])]
        return cls(**dados)
