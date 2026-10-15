from trabalho1.cadastro import Inventario as InventarioAnterior
from trabalho1.validacoes import numero

from .modelos import criar_equipamento


class Inventario(InventarioAnterior):
    def __init__(self, ativos=None):
        super().__init__(ativos)
        self.validar_dependencias()

    def validar_dependencias(self):
        for ativo in self.ativos.values():
            if any(id_ativo not in self.ativos for id_ativo in ativo.dependencias):
                raise ValueError("A dependência aponta para um ativo inexistente.")

    def cadastrar_ativo(
        self,
        id,
        nome,
        responsavel,
        setor,
        tipo,
        criticidade="MEDIA",
        status="ATIVO",
        descricao="",
        vulnerabilidades=None,
        dependencias=None,
        **campos,
    ):
        dados = {
            "id": id,
            "nome": nome,
            "responsavel": responsavel,
            "setor": setor,
            "tipo": tipo,
            "criticidade": criticidade,
            "status": status,
            "descricao": descricao,
            "vulnerabilidades": [] if vulnerabilidades is None else vulnerabilidades,
            "dependencias": {} if dependencias is None else dependencias,
        }
        dados.update(campos)
        ativo = criar_equipamento(dados)
        if any(id_ativo not in self.ativos for id_ativo in ativo.dependencias):
            raise ValueError("Ativo da dependência não encontrado.")
        return self.cadastrar_ativo_objeto(ativo)

    def atualizar_ativo(self, id, **campos):
        ativo = self.buscar_ativo(id=id)
        if ativo is None:
            raise LookupError("Ativo não encontrado.")
        permitidos = {
            "nome",
            "responsavel",
            "setor",
            "tipo",
            "criticidade",
            "status",
            "descricao",
        }
        if not campos or not campos.keys() <= permitidos:
            raise ValueError("Informe apenas campos que podem ser alterados.")
        antes = ativo.dados()
        alterado = criar_equipamento({**antes, **campos})
        if any(
            item.id != ativo.id and item.nome.casefold() == alterado.nome.casefold()
            for item in self.ativos.values()
        ):
            raise ValueError("Já existe um ativo com esse nome.")
        self.ativos[ativo.id] = alterado
        self._registrar(
            "atualizacao",
            ativo.id,
            {campo: antes[campo] for campo in campos},
            {campo: alterado.dados()[campo] for campo in campos},
        )
        return alterado

    def definir_dependencia(self, id, id_ativo, peso):
        ativo = self.buscar_ativo(id=id)
        if ativo is None or self.buscar_ativo(id=id_ativo) is None:
            raise LookupError("Ativo não encontrado.")
        id_ativo = numero(id_ativo, "ID da dependência")
        dados = ativo.dados()
        dados["dependencias"] = {**ativo.dependencias, id_ativo: peso}
        alterado = criar_equipamento(dados)
        self.ativos[ativo.id] = alterado
        self._registrar("dependencia", ativo.id)
        return alterado

    def remover_dependencia(self, id, id_ativo):
        ativo = self.buscar_ativo(id=id)
        id_ativo = numero(id_ativo, "ID da dependência")
        if ativo is None or id_ativo not in ativo.dependencias:
            raise LookupError("Dependência não encontrada.")
        del ativo.dependencias[id_ativo]
        self._registrar("remocao_dependencia", ativo.id)

    def excluir_ativo(self, id, confirmar=False):
        id = numero(id, "ID do ativo")
        if self.buscar_ativo(id=id) is None:
            raise LookupError("Ativo não encontrado.")
        removido = super().excluir_ativo(id, confirmar)
        if removido:
            for ativo in self.ativos.values():
                ativo.dependencias.pop(id, None)
        return removido
