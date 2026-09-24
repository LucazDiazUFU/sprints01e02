from datetime import datetime, timezone

from .modelos import Ativo, Vulnerabilidade
from .validacoes import CRITICIDADES, SEVERIDADES, STATUS_ATIVO, STATUS_VULNERABILIDADE, cve, cvss, numero, opcao, texto, tipo_ativo


class Inventario:
    def __init__(self, ativos=None):
        self.ativos = {}
        self.historico = []
        for ativo in ativos or []:
            self.cadastrar_ativo_objeto(ativo)
        self.historico.clear()

    def cadastrar_ativo_objeto(self, ativo):
        if ativo.id in self.ativos:
            raise ValueError("Já existe um ativo com esse ID.")
        if any(item.nome.casefold() == ativo.nome.casefold() for item in self.ativos.values()):
            raise ValueError("Já existe um ativo com esse nome.")
        ids = {v.id for item in self.ativos.values() for v in item.vulnerabilidades}
        if len({v.id for v in ativo.vulnerabilidades}) != len(ativo.vulnerabilidades) or ids.intersection(v.id for v in ativo.vulnerabilidades):
            raise ValueError("ID de vulnerabilidade duplicado.")
        self.ativos[ativo.id] = ativo
        self._registrar("cadastro", ativo.id)
        return ativo

    def cadastrar_ativo(self, id, nome, responsavel, setor, tipo, criticidade="MEDIA", status="ATIVO", descricao="", vulnerabilidades=None):
        ativo = Ativo(id, nome, responsavel, setor, tipo, criticidade, status, descricao, vulnerabilidades or [])
        return self.cadastrar_ativo_objeto(ativo)

    def buscar_ativo(self, id=None, nome=None):
        if id is not None:
            return self.ativos.get(numero(id, "ID do ativo"))
        if nome is not None:
            nome = texto(nome, "Nome").casefold()
            return next((ativo for ativo in self.ativos.values() if ativo.nome.casefold() == nome), None)
        raise ValueError("Informe o ID ou o nome do ativo.")

    def listar_ativos(self, nome="", tipo=None, criticidade=None, status=None):
        itens = self.ativos.values()
        if nome:
            itens = [item for item in itens if nome.casefold() in item.nome.casefold()]
        if tipo is not None:
            codigo = tipo_ativo(tipo)
            itens = [item for item in itens if item.tipo == codigo]
        if criticidade:
            valor = opcao(criticidade, CRITICIDADES, "Criticidade")
            itens = [item for item in itens if item.criticidade == valor]
        if status:
            valor = opcao(status, STATUS_ATIVO, "Status")
            itens = [item for item in itens if item.status == valor]
        return sorted(itens, key=lambda item: item.id)

    def atualizar_ativo(self, id, **campos):
        ativo = self.buscar_ativo(id=id)
        if ativo is None:
            raise ValueError("Ativo não encontrado.")
        permitidos = {"nome", "responsavel", "setor", "tipo", "criticidade", "status", "descricao"}
        if not campos or not set(campos) <= permitidos:
            raise ValueError("Informe apenas campos que podem ser alterados.")
        antes = ativo.dados()
        novos = {**antes, **campos}
        alterado = Ativo.carregar(novos)
        if alterado.nome.casefold() != ativo.nome.casefold() and any(item.nome.casefold() == alterado.nome.casefold() for item in self.ativos.values() if item.id != ativo.id):
            raise ValueError("Já existe um ativo com esse nome.")
        self.ativos[ativo.id] = alterado
        self._registrar("atualizacao", ativo.id, {campo: antes[campo] for campo in campos}, {campo: alterado.dados()[campo] for campo in campos})
        return alterado

    def excluir_ativo(self, id, confirmar=False):
        ativo = self.buscar_ativo(id=id)
        if ativo is None:
            raise ValueError("Ativo não encontrado.")
        if not confirmar:
            return False
        del self.ativos[ativo.id]
        self._registrar("exclusao", ativo.id)
        return True

    def cadastrar_vulnerabilidade(self, ativo_id, id, descricao, categoria, severidade, status="ABERTA", cve="", cvss=None, referencia="", recomendacao=""):
        ativo = self.buscar_ativo(id=ativo_id)
        if ativo is None:
            raise ValueError("Ativo não encontrado.")
        vulnerabilidade = Vulnerabilidade(id, descricao, categoria, severidade, status, cve, cvss, referencia, recomendacao)
        if self.localizar_vulnerabilidade(vulnerabilidade.id):
            raise ValueError("Já existe uma vulnerabilidade com esse ID.")
        ativo.vulnerabilidades.append(vulnerabilidade)
        self._registrar("cadastro_vulnerabilidade", ativo.id)
        return vulnerabilidade

    def localizar_vulnerabilidade(self, id):
        id = numero(id, "ID da vulnerabilidade")
        for ativo in self.ativos.values():
            for vulnerabilidade in ativo.vulnerabilidades:
                if vulnerabilidade.id == id:
                    return ativo, vulnerabilidade
        return None

    def listar_vulnerabilidades(self, ativo_id=None, cve_codigo="", severidade=None, status=None):
        ativos = [self.buscar_ativo(id=ativo_id)] if ativo_id is not None else self.ativos.values()
        if ativo_id is not None and ativos[0] is None:
            raise ValueError("Ativo não encontrado.")
        itens = [(ativo, vuln) for ativo in ativos for vuln in ativo.vulnerabilidades]
        if cve_codigo:
            codigo = cve(cve_codigo)
            itens = [(ativo, vuln) for ativo, vuln in itens if vuln.cve == codigo]
        if severidade:
            valor = opcao(severidade, SEVERIDADES, "Severidade")
            itens = [(ativo, vuln) for ativo, vuln in itens if vuln.severidade == valor]
        if status:
            valor = opcao(status, STATUS_VULNERABILIDADE, "Status")
            itens = [(ativo, vuln) for ativo, vuln in itens if vuln.status == valor]
        ordem = {"CRITICA": 0, "ALTA": 1, "MEDIA": 2, "BAIXA": 3}
        return sorted(itens, key=lambda par: (ordem[par[1].severidade], par[0].id, par[1].id))

    def atualizar_vulnerabilidade(self, id, **campos):
        encontrado = self.localizar_vulnerabilidade(id)
        if encontrado is None:
            raise ValueError("Vulnerabilidade não encontrada.")
        ativo, vulnerabilidade = encontrado
        permitidos = {"descricao", "categoria", "severidade", "status", "cve", "cvss", "referencia", "recomendacao"}
        if not campos or not set(campos) <= permitidos:
            raise ValueError("Informe apenas campos que podem ser alterados.")
        antes = vulnerabilidade.dados()
        alterada = Vulnerabilidade(**{**antes, **campos})
        posicao = ativo.vulnerabilidades.index(vulnerabilidade)
        ativo.vulnerabilidades[posicao] = alterada
        self._registrar("atualizacao_vulnerabilidade", ativo.id, {campo: antes[campo] for campo in campos}, {campo: alterada.dados()[campo] for campo in campos})
        return alterada

    def excluir_vulnerabilidade(self, id, confirmar=False):
        encontrado = self.localizar_vulnerabilidade(id)
        if encontrado is None:
            raise ValueError("Vulnerabilidade não encontrada.")
        if not confirmar:
            return False
        ativo, vulnerabilidade = encontrado
        ativo.vulnerabilidades.remove(vulnerabilidade)
        self._registrar("exclusao_vulnerabilidade", ativo.id)
        return True

    def _registrar(self, acao, ativo_id, antes=None, depois=None):
        registro = {"data": datetime.now(timezone.utc).isoformat(), "acao": acao, "ativo_id": ativo_id}
        if antes is not None:
            registro["antes"] = antes
            registro["depois"] = depois
        self.historico.append(registro)
