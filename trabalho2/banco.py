from contextlib import contextmanager
from pathlib import Path
import sqlite3

from .cadastro import Inventario
from .modelos import criar_equipamento


class VersaoDesatualizada(ValueError):
    pass


class RepositorioSQL:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.conectar() as conexao:
            conexao.executescript(
                Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
            )

    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.caminho, timeout=10)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        try:
            with conexao:
                yield conexao
        finally:
            conexao.close()

    def carregar(self):
        with self.conectar() as conexao:
            conexao.execute("BEGIN")
            versao = conexao.execute(
                "SELECT versao FROM controle WHERE id = 1"
            ).fetchone()[0]
            dados = {
                item["id"]: {**dict(item), "vulnerabilidades": [], "dependencias": {}}
                for item in conexao.execute("SELECT * FROM equipamentos ORDER BY id")
            }
            for item in conexao.execute("SELECT * FROM vulnerabilidades ORDER BY id"):
                vulnerabilidade = dict(item)
                id_ativo = vulnerabilidade.pop("ativo_id")
                dados[id_ativo]["vulnerabilidades"].append(vulnerabilidade)
            for item in conexao.execute("SELECT * FROM dependencias"):
                dados[item["ativo_id"]]["dependencias"][item["dependencia_id"]] = item[
                    "peso"
                ]
            inventario = Inventario(
                [criar_equipamento(item) for item in dados.values()]
            )
            inventario.versao = versao
            return inventario

    def salvar(self, inventario):
        inventario.validar_dependencias()
        with self.conectar() as conexao:
            conexao.execute("BEGIN IMMEDIATE")
            atual = conexao.execute(
                "SELECT versao FROM controle WHERE id = 1"
            ).fetchone()[0]
            if getattr(inventario, "versao", atual) != atual:
                raise VersaoDesatualizada("A base mudou. Recarregue e tente novamente.")
            conexao.execute("DELETE FROM dependencias")
            conexao.execute("DELETE FROM vulnerabilidades")
            conexao.execute("DELETE FROM equipamentos")
            for ativo in inventario.listar_ativos():
                conexao.execute(
                    "INSERT INTO equipamentos VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        ativo.id,
                        ativo.nome,
                        ativo.responsavel,
                        ativo.setor,
                        ativo.tipo,
                        ativo.criticidade,
                        ativo.status,
                        ativo.descricao,
                    ),
                )
                for item in ativo.vulnerabilidades:
                    conexao.execute(
                        "INSERT INTO vulnerabilidades "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            item.id,
                            ativo.id,
                            item.descricao,
                            item.categoria,
                            item.severidade,
                            item.status,
                            item.cve,
                            item.cvss,
                            item.referencia,
                            item.recomendacao,
                        ),
                    )
            for ativo in inventario.listar_ativos():
                conexao.executemany(
                    "INSERT INTO dependencias VALUES (?, ?, ?)",
                    [
                        (ativo.id, id_ativo, peso)
                        for id_ativo, peso in ativo.dependencias.items()
                    ],
                )
            conexao.execute("UPDATE controle SET versao = versao + 1 WHERE id = 1")
        inventario.versao = atual + 1
