from contextlib import contextmanager
import json

import pymysql

from .banco import VersaoDesatualizada
from .cadastro import Inventario
from .configuracao import ConfiguracaoBanco
from .modelos import criar_equipamento


class RepositorioMariaDB:
    def __init__(self, configuracao=None):
        self.configuracao = configuracao or ConfiguracaoBanco.ambiente()
        with self.conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT versao FROM trabalho2_controle WHERE id = 1")
                if cursor.fetchone() is None:
                    raise ValueError("Inicialize o banco com deploy/schema_mariadb.sql.")

    @contextmanager
    def conectar(self):
        conexao = pymysql.connect(**self.configuracao.parametros())
        try:
            yield conexao
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def carregar(self):
        with self.conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
                conexao.begin()
                cursor.execute("SELECT versao FROM trabalho2_controle WHERE id = 1")
                versao = cursor.fetchone()[0]
                cursor.execute("SELECT dados FROM trabalho2_equipamentos ORDER BY id")
                dados = [json.loads(item[0]) for item in cursor.fetchall()]
        inventario = Inventario([criar_equipamento(item) for item in dados])
        inventario.versao = versao
        return inventario

    def salvar(self, inventario):
        inventario.validar_dependencias()
        itens = [
            (ativo.id, json.dumps(ativo.dados(), ensure_ascii=False, allow_nan=False))
            for ativo in inventario.listar_ativos()
        ]
        with self.conectar() as conexao:
            conexao.begin()
            with conexao.cursor() as cursor:
                cursor.execute(
                    "SELECT versao FROM trabalho2_controle WHERE id = 1 FOR UPDATE"
                )
                atual = cursor.fetchone()[0]
                if getattr(inventario, "versao", atual) != atual:
                    raise VersaoDesatualizada("A base mudou. Recarregue e tente novamente.")
                cursor.execute("DELETE FROM trabalho2_equipamentos")
                if itens:
                    cursor.executemany(
                        "INSERT INTO trabalho2_equipamentos (id, dados) VALUES (%s, %s)",
                        itens,
                    )
                cursor.execute(
                    "UPDATE trabalho2_controle SET versao = versao + 1 WHERE id = 1"
                )
        inventario.versao = atual + 1
